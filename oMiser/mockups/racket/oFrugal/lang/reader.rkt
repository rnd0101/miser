#lang racket/base
(provide read-syntax)

(require racket/list racket/match racket/port racket/string syntax/strip-context)

(define (char-alphanumeric? c)
  (or (char-alphabetic? c) (char-numeric? c)))


;; -----------------------
;; Tokenizer
;; -----------------------

(struct tok (type val) #:transparent)

(define (tokenize s)
  (define len (string-length s))
  (define i 0)
  (define toks '())

  (define (peek) (if (< i len) (string-ref s i) #\nul))
  (define (advance!) (set! i (add1 i)))
  (define (add! t v) (set! toks (cons (tok t v) toks)))

  (define (skip-ws!)
    (let loop ()
      (when (and (< i len) (char-whitespace? (peek)))
        (advance!) (loop))))

  (define (read-while pred)
    (define start i)
    (let loop ()
      (when (and (< i len) (pred (peek)))
        (advance!) (loop)))
    (substring s start i))

  (let loop ()
    (skip-ws!)
    (cond
      [(>= i len) (reverse (cons (tok 'EOF "") toks))]

      [(and (char=? (peek) #\:) (< (add1 i) len)
            (char=? (string-ref s (add1 i)) #\:))
       (set! i (+ i 2))
       (add! 'COLON2 "::")
       (loop)]

      [(char=? (peek) #\`)
       (advance!)
       (add! 'QUOTE "`")
       (loop)]

      [(char=? (peek) #\‵)
       (advance!)
       (add! 'QUOTE "‵")
       (loop)]

      [(char=? (peek) #\()
       (advance!) (add! 'LP "(") (loop)]
      [(char=? (peek) #\))
       (advance!) (add! 'RP ")") (loop)]
      [(char=? (peek) #\[)
       (advance!) (add! 'LB "[") (loop)]
      [(char=? (peek) #\])
       (advance!) (add! 'RB "]") (loop)]
      [(char=? (peek) #\,)
       (advance!) (add! 'COMMA ",") (loop)]
      [(char=? (peek) #\;)
       (advance!) (add! 'SEMI ";") (loop)]
      [(char=? (peek) #\=)
       (advance!) (add! 'EQ "=") (loop)]

      [(char=? (peek) #\.)
       (advance!)
       (define name (read-while (λ (c) (or (char-alphanumeric? c) (char=? c #\_)))))
       (add! 'PRIM (string-append "." name))
       (loop)]

      [(char=? (peek) #\^)
       (advance!)
       (define name (read-while (λ (c) (or (char-alphanumeric? c) (char=? c #\_)))))
       (add! 'VAR (string-append "^" name))
       (loop)]

      [(or (char-alphanumeric? (peek)) (char=? (peek) #\_))
       (define name (read-while (λ (c) (or (char-alphanumeric? c) (char=? c #\_)))))
       (add! 'LINDY name)
       (loop)]

      [else
       (error 'tokenize (format "unexpected character: ~a" (peek)))])))

;; -----------------------
;; Recursive-descent parser
;; AST nodes are plain lists:
;;  (lindy "x") | (prim ".NIL") | (var "^x")
;;  (enc e) | (pair a b) | (app f x)
;;  (assign "x" expr)
;; -----------------------

(define toks #f)
(define pos 0)

(define (cur) (list-ref toks pos))
(define (cur-type) (tok-type (cur)))
(define (cur-val) (tok-val (cur)))

(define (eat! t)
  (unless (eq? (cur-type) t)
    (error 'parse (format "expected ~a, got ~a" t (cur-type))))
  (define v (cur-val))
  (set! pos (add1 pos))
  v)

(define (starts-unary? t)
  (memq t '(LINDY PRIM VAR QUOTE LP LB)))

(define (parse-program)
  (define stmts '())
  (let loop ()
    (unless (eq? (cur-type) 'EOF)
      (set! stmts (cons (parse-statement) stmts))
      (when (eq? (cur-type) 'SEMI) (eat! 'SEMI))
      (loop)))
  (reverse stmts))

(define (parse-statement)
  (cond
    [(and (eq? (cur-type) 'LINDY) (string-ci=? (cur-val) "ob"))
     (eat! 'LINDY) ; "ob"
     (define v (eat! 'VAR))
     (eat! 'EQ)
     (define e (parse-binary))
     (list 'assign v e)]
    [else (parse-binary)]))

;; binary := app ("::" binary)?   right associative
(define (parse-binary)
  (define left (parse-app))
  (if (eq? (cur-type) 'COLON2)
      (begin
        (eat! 'COLON2)
        (list 'pair left (parse-binary)))
      left))

;; app := unary unary*    left associative
(define (parse-app)
  (define f (parse-unary))
  (let loop ([acc f])
    (if (starts-unary? (cur-type))
        (let ([arg (parse-unary)])
          (loop (list 'app acc arg)))
        acc)))

;; unary := QUOTE unary | list | "(" binary ")" | term
(define (parse-unary)
  (match (cur-type)
    ['QUOTE
     (eat! 'QUOTE)
     (list 'enc (parse-unary))]
    ['LB (parse-list)]
    ['LP
     (eat! 'LP)
     (define e (parse-binary))
     (eat! 'RP)
     e]
    [else (parse-term)]))

(define (parse-list)
  (eat! 'LB)
  (define items '())
  (unless (eq? (cur-type) 'RB)
    (set! items (cons (parse-binary) items))
    (let loop ()
      (when (eq? (cur-type) 'COMMA)
        (eat! 'COMMA)
        (set! items (cons (parse-binary) items))
        (loop))))
  (eat! 'RB)
  (list 'list (reverse items)))

(define (parse-term)
  (match (cur-type)
    ['LINDY (list 'lindy (eat! 'LINDY))]
    ['PRIM  (list 'prim (eat! 'PRIM))]
    ['VAR   (list 'var (eat! 'VAR))]
    [else (error 'parse-term "expected term")]))

;; -----------------------
;; Compilation to Racket syntax using omiser/runtime
;; -----------------------

(define (prim->id pstr)
  ;; ".NIL" -> 'NIL, ".ARG" -> 'ARG, etc.
  (string->symbol (substring pstr 1)))

(define (var->id vstr)
  (string->symbol (substring vstr 1)))

(define (compile ast)
  (match ast
    [(list 'lindy s) #`(L #,s)]
    [(list 'prim p)  #`#,(prim->id p)]
    [(list 'var v)   #`#, (var->id v)]
    [(list 'enc e)   #`(e #,(compile e))]
    [(list 'pair a b) #`(c #,(compile a) #,(compile b))]
    [(list 'app f x) #`(ap #,(compile f) #,(compile x))]
    [(list 'list items)
     ;; consify ending in NIL
     (define compiled (map compile items))
     (define (fold-right xs tail)
       (if (null? xs) tail
           #`(c #,(car xs) #,(fold-right (cdr xs) tail))))
     (fold-right compiled #'NIL)]
    [(list 'assign v e)
     #`(define #,(var->id v) #,(compile e))]
    [else (error 'compile (format "unknown AST ~a" ast))]))

(define (read-syntax path port)
  (define src (port->string port))
  (define asts
    (begin
      (set! toks (tokenize src))
      (set! pos 0)
      (parse-program)))

  (define compiled (map compile asts))

;; Wrap non-assignments so they print when they evaluate to an ob.
(define (wrap-for-print stx)
  (syntax-case stx (define)
    [(define _ _) stx] ; assignment stays a definition
    [expr
     #`(let ([v expr])
         (when (ob? v)
           (displayln (ob->cfob (eval-top v)))))]))

(define forms (map wrap-for-print compiled))
 (strip-context
 #`(module oFrugal-module racket/base
     (require omiser/runtime)
     #,@forms))
)

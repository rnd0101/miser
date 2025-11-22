#lang racket/base
;; structs + constructors
(provide ob?
         Lindy?
         Ind?
         Pair?
         Enc?
         (struct-out Lindy)
         (struct-out Ind)
         (struct-out Pair)
         (struct-out Enc)
         L
         c
         e
         ;; projections + predicates
         ob-a
         ob-b
         is-singleton?
         is-individual?
         is-pair?
         is-lindy?
         is-enc?
         ;; primitives
         NIL
         A
         B
         C
         D
         E
         SELF
         ARG
         EV
         ;; semantics
         ap
         ev
         eval-top
         ;; printing
         ob->cfob)

(require racket/match
         racket/list)

;; -----------------------
;; Core data representations
;; -----------------------

(struct Lindy (name) #:transparent)
(struct Ind (name ap-proc ev-proc) #:transparent)
(struct Pair (a b) #:transparent)
(struct Enc (a) #:transparent)

(define (ob? x)
  (or (Lindy? x) (Ind? x) (Pair? x) (Enc? x)))

;; Projections
(define (ob-a z)
  (match z
    [(Pair x _) x]
    [(Enc x) x]
    [_ z]))

(define (ob-b z)
  (match z
    [(Pair _ y) y]
    [(Enc _) z] ; singleton self-loop
    [_ z]))

(define (is-singleton? x)
  (equal? (ob-b x) x))
(define (is-individual? x)
  (and (equal? (ob-a x) x) (equal? (ob-b x) x)))
(define (is-pair? x)
  (Pair? x))
(define (is-lindy? x)
  (Lindy? x))
(define (is-enc? x)
  (and (is-singleton? x) (not (is-individual? x))))

;; Constructors matching ob.c / ob.e / L(...)
(define (c x y)
  (Pair x y))
(define (e x)
  (Enc x))
(define (L s)
  (Lindy s))

;; -----------------------
;; Pure lindy trace flag
;; -----------------------

(define (pure-lindy-trace? z)
  (match z
    [(Lindy _) #t]
    [(Pair a b) (and (pure-lindy-trace? a) (pure-lindy-trace? b))]
    [_ #f]))

;; -----------------------
;; Default behaviors
;; -----------------------

;; default ap: trace c(e(p), e(x))
(define (default-ap p x)
  (c (e p) (e x)))

;; mk-prim makes an Ind whose default ev returns itself (2-arity),
;; like Python ob.ev returning self unless overridden.
(define (mk-prim name ap-proc [ev-proc #f])
  (letrec ([self (Ind name ap-proc (or ev-proc (λ (p x) self)))])
    self))

;; -----------------------
;; Primitive individuals (final, arity + letrec safe)
;; -----------------------

;; Primitives that override ap directly:
(define NIL (mk-prim 'NIL (λ (x) x)))
(define A (mk-prim 'A (λ (x) (ob-a x))))
(define B (mk-prim 'B (λ (x) (ob-b x))))
(define E (mk-prim 'E (λ (x) (e x))))

;; Self-referential primitives:
;; They must capture self only inside lambdas.

(define EV
  (letrec ([self (Ind 'EV
                      (λ (x) (default-ap self x)) ; unary trace ap
                      (λ (p x) self))]) ; eval to itself
    self))

(define SELF
  (letrec ([self (Ind 'SELF
                      (λ (x) (default-ap self x)) ; unary trace ap
                      (λ (p x) p))]) ; eval-slot
    self))

(define ARG
  (letrec ([self (Ind 'ARG
                      (λ (x) (default-ap self x)) ; unary trace ap
                      (λ (p x) x))]) ; eval-slot
    self))

;; C and D override ap but refer to themselves:
(define C
  (letrec ([self (Ind 'C (λ (x) (c self (c (e x) ARG))) (λ (p x) self))])
    self))

(define D
  (letrec ([self (Ind 'D (λ (x) (c self (c (e x) ARG))) (λ (p x) self))])
    self))

;; -----------------------
;; ap / ev semantics
;; -----------------------

(define (ap p x)
  (match p
    [(Lindy _)
     (if (pure-lindy-trace? x)
         (c p x)
         (c p (e x)))]
    [(Enc a) a]
    [(Ind _ ap-proc _) (ap-proc x)]
    [(Pair _ _)
     (if (pure-lindy-trace? (c p x))
         (c p x)
         (ev p x p))]
    [_ (default-ap p x)]))

(define (ev p x exp)
  (match exp
    [(Enc a) a]
    [(Ind _ _ ev-proc) (ev-proc p x)]
    [(Pair a b)
     (cond
       [(and (equal? a C) (Pair? b)) (c (ev p x (Pair-a b)) (ev p x (Pair-b b)))]
       [(and (equal? a D) (Pair? b)) (if (equal? (ev p x (Pair-a b)) (ev p x (Pair-b b))) A B)]
       [(equal? a EV) (ev p x (ev p x b))]
       [else (ap (ev p x a) (ev p x b))])]
    [_ exp]))

(define (eval-top exp)
  (ev SELF ARG exp))

;; -----------------------
;; CFob-ish pretty printer
;; -----------------------

(define (ob->cfob z)
  (define (term t)
    (match t
      [(Lindy s) (format "~a" s)]
      [(Ind n _ _) (format ".~a" n)]
      [_ "?!"]))
  (define (unary u)
    (cond
      [(is-individual? u) (term u)]
      [(is-enc? u) (string-append "`" (unary (ob-a u)))]
      [(is-pair? u) (string-append "(" (canonical u) ")")]
      [else (term u)]))
  (define (canonical x)
    (if (is-pair? x)
        (string-append (unary (ob-a x)) " :: " (canonical (ob-b x)))
        (unary x)))
  (canonical z))

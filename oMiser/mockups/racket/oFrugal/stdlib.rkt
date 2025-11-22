#lang racket/base
(require omiser/runtime)

(provide cI
         cK
         cSpart
         cS
         cREV
         cB0
         cB
         cC
         cD
         cT
         cUobAB
         cW0
         cW
         cY
         hasX
         has
         simpleSwap
         swap
         dup
         bTRUE
         bFALSE
         bNOT
         bOR
         bAND
         bXOR
         bSAY
         isIndividual
         A
         ARG
         B
         C
         D
         E
         EV
         NIL
         SELF
         namespace)

(define cI NIL)

(define cK (c E ARG))

(define cSpart (c C (c (c E ARG) (e ARG))))

(define cS
  (c C (c (e C) (c C (c (c E (c C (c (c E ARG) (e ARG)))) (e (c C (c (c E ARG) (e ARG)))))))))

(define cREV
  (c (c (e (e (c C
                 (c (e (c (e (c (c (e (c E ARG)) ARG) (c (e (c E ARG)) ARG))) ARG))
                    (c C (c (c E ARG) (e ARG)))))))
        ARG)
     (c (e (c E ARG)) ARG)))

(define cB0
  (c (c (e (e (c C
                 (c (e C)
                    (c C (c (c E (c C (c (c E ARG) (e ARG)))) (e (c C (c (c E ARG) (e ARG))))))))))
        ARG)
     (c (e (c E ARG)) ARG)))

(define cB (c C (c (e C) (c C (c (c E (c E ARG)) (e (c C (c (c E ARG) (e ARG)))))))))

(define cC (c C (c (e C) (c C (c (c E (c E ARG)) (e (c C (c (e ARG) (c E ARG)))))))))

(define cD
  (c C
     (c (e (e (c C (c (e C) (c C (c (c E (c E ARG)) (e (c C (c (c E ARG) (e ARG))))))))))
        (c C (c (c E ARG) (e ARG))))))

(define cT (c C (c (e ARG) (c E ARG))))

(define cUobAB (c ARG (e (c E (e NIL)))))

(define cW0
  (c (c (e (c C
              (c (e C) (c C (c (c E (c C (c (c E ARG) (e ARG)))) (e (c C (c (c E ARG) (e ARG)))))))))
        ARG)
     (c (e (c C (c (e (c (e (c E ARG)) ARG)) (c C (c (c E ARG) (e ARG)))))) ARG)))

(define cW (c C (c (c C ARG) (e ARG))))

(define cY (c C (c (c C (c (c E ARG) (e SELF))) (e ARG))))

(define hasX
  (c EV
     (c (c D (c ARG (c B ARG)))
        (e (c B (c EV (c (c D (c (e (L "X")) (c A ARG))) (e (c A (c SELF (c B ARG)))))))))))

(define has
  (c C
     (c (e EV)
        (c C
           (c (e (c D (c ARG (c B ARG))))
              (c E
                 (c C
                    (c B
                       (c C
                          (c (e EV)
                             (c C
                                (c (c C (c (e D) (c C (c (c E ARG) (e (c A ARG))))))
                                   (c E (e (c A (c SELF (c B ARG)))))))))))))))))

(define simpleSwap (c (c B ARG) (c A ARG)))

(define swap (c EV (c (c D (c ARG (c B ARG))) (e (c ARG (c C (c (c B ARG) (c A ARG))))))))

(define dup (c C (c ARG ARG)))

(define bTRUE A)

(define bFALSE B)

(define bNOT (c EV (c D B)))

(define bOR (c (c C ARG) (c C A)))

(define bAND (c ARG (c E B)))

(define bXOR (c (c ARG (c D B)) B))

(define bSAY (c (L "TRUE") (L "FALSE")))

(define isIndividual (c D (c ARG (c B ARG))))

(define namespace
  (hash 'cI
        cI
        'cK
        cK
        'cSpart
        cSpart
        'cS
        cS
        'cREV
        cREV
        'cB0
        cB0
        'cB
        cB
        'cC
        cC
        'cD
        cD
        'cT
        cT
        'cUobAB
        cUobAB
        'cW0
        cW0
        'cW
        cW
        'cY
        cY
        'hasX
        hasX
        'has
        has
        'simpleSwap
        simpleSwap
        'swap
        swap
        'dup
        dup
        'bTRUE
        bTRUE
        'bFALSE
        bFALSE
        'bNOT
        bNOT
        'bOR
        bOR
        'bAND
        bAND
        'bXOR
        bXOR
        'bSAY
        bSAY
        'isIndividual
        isIndividual
        'A
        A
        'ARG
        ARG
        'B
        B
        'C
        C
        'D
        D
        'E
        E
        'EV
        EV
        'NIL
        NIL
        'SELF
        SELF))

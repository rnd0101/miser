from miser import c, E, ARG, C, e, ob, NIL, EV, D, B, SELF, A, L

# cI = c(c(e(c(E, ARG)), ARG), c(e(c(E, ARG)), ARG))
cI = NIL
cK = c(E, ARG)  # K-combinator
cSpart = c(C, c(cK, e(ARG)))
cS = c(C, c(e(C), c(C, c(c(E, cSpart), e(cSpart)))))  # S-combinator

# Buggy:
# cREV = (^cS(^cK(^cS(^cI))))(^cK)
cREV = c(c(e(e(c(C, c(e(c(e(c(c(e(c(E, ARG)), ARG), c(e(c(E, ARG)), ARG))), ARG)), c(C, c(c(E, ARG), e(ARG))))))), ARG),
         c(e(c(E, ARG)), ARG))

# BCKW system

# B = S (K S) K
cB0 = c(c(e(e(c(C, c(e(C), c(C, c(c(E, c(C, c(c(E, ARG), e(ARG)))), e(c(C, c(c(E, ARG), e(ARG)))))))))), ARG),
       c(e(c(E, ARG)), ARG))

# Optimized
# cB = C ** (((B ** E) ** (C ** ARG)) ** e((C ** ARG)))  - buggy
cB = (C ** (e(C) ** (C ** ((E ** (E ** ARG)) ** e((C ** ((E ** ARG) ** e(ARG))))))))

# C = S (S (K (S (K S) K)) S) (K K)

# .C :: `.C :: .C :: ( .E :: .E :: .ARG ) :: `( .C :: `.ARG :: .E :: .ARG )
cC = (C ** (e(C) ** (C ** ((E ** (E ** ARG)) ** e((C ** (e(ARG) ** (E ** ARG))))))))

# (.C :: (`(`((.C :: (`(.C) :: (.C :: ((.E :: (.E :: .ARG)) :: `((.C :: ((.E :: .ARG) :: `(.ARG)))))))))) :: (.C :: ((.E :: .ARG) :: `(.ARG)))))
cD = (C ** (e(e((C ** (e(C) ** (C ** ((E ** (E ** ARG)) ** e((C ** ((E ** ARG) ** e(ARG)))))))))) ** (C ** ((E ** ARG) ** e(ARG)))))

#
# (.C :: (`(.ARG) :: (.E :: .ARG)))
cT = (C ** (e(ARG) ** (E ** ARG)))

# .ARG :: `(.E :: `.NIL)
cUobAB = (ARG ** e((E ** e(NIL))))

# W = S S (S K)
cW0 = c(c(e(c(C, c(e(C), c(C, c(c(E, c(C, c(c(E, ARG), e(ARG)))), e(c(C, c(c(E, ARG), e(ARG))))))))), ARG),
       c(e(c(C, c(e(c(e(c(E, ARG)), ARG)), c(C, c(c(E, ARG), e(ARG)))))), ARG))

# Optimized
cW = C ** ((C ** ARG) ** e(ARG))

# (.C :: ((.C :: ((.E :: .ARG) :: `(.SELF))) :: `(.ARG)))
cY = (C ** ((C ** ((E ** ARG) ** e(SELF))) ** e(ARG)))

# TODO: iota
# cIOTA = ...

#
hasX = EV ** (D ** ARG ** B ** ARG) \
       ** e(B ** (EV ** (D ** e(L("X")) ** A ** ARG)
                  ** e(A ** (SELF ** B ** ARG))
                  ))

has = (
        C ** e(EV)
        ** C ** e(D ** ARG ** B ** ARG)
        ** E ** C ** B
        ** C ** e(EV)
        ** C ** (C ** e(D)
                 ** (C ** (E ** ARG)
                     ** e(A ** ARG)))
        ** E ** e(A ** SELF ** B ** ARG)
)

simpleSwap = (B ** ARG) ** (A ** ARG)
swap = c(EV, c(c(D, c(ARG, c(B, ARG))), e(c(ARG, c(C, c(c(B, ARG), c(A, ARG)))))))
dup = C ** ARG ** ARG

# Some boolean operators
bTRUE = A
bFALSE = B
bNOT = EV ** (D ** B)
bOR = (C ** ARG) ** (C ** A)
bAND = ARG ** (E ** B)
bXOR = (ARG ** (D ** B)) ** B
bSAY = L("TRUE") ** L("FALSE")

isIndividual = (D ** ARG ** B ** ARG)

namespace = {k: v for k, v in list(vars().items()) if isinstance(v, ob)}

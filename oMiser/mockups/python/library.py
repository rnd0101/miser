from miser import c, E, ARG, C, e, ob

cI = c(c(e(c(E, ARG)), ARG), c(e(c(E, ARG)), ARG))
cK = c(E, ARG)  # K-combinator
cSpart = c(C, c(cK, e(ARG)))
cS = c(C, c(e(C), c(C, c(c(E, cSpart), e(cSpart)))))  # S-combinator

# Buggy:
#cREV = (^cS(^cK(^cS(^cI))))(^cK)
cREV = c(c(e(e(c(C, c(e(c(e(c(c(e(c(E, ARG)), ARG), c(e(c(E, ARG)), ARG))), ARG)), c(C, c(c(E, ARG), e(ARG))))))), ARG), c(e(c(E, ARG)), ARG))

# BCKW system

# B = S (K S) K
cB = c(c(e(e(c(C, c(e(C), c(C, c(c(E, c(C, c(c(E, ARG), e(ARG)))), e(c(C, c(c(E, ARG), e(ARG)))))))))), ARG), c(e(c(E, ARG)), ARG))

# C = S (S (K (S (K S) K)) S) (K K)
cC = c(c(e(c(c(e(e(c(c(e(e(c(C, c(e(C), c(C, c(c(E, c(C, c(c(E, ARG), e(ARG)))), e(c(C, c(c(E, ARG), e(ARG)))))))))), ARG), c(e(c(E, ARG)), ARG)))), ARG), c(e(c(C, c(e(C), c(C, c(c(E, c(C, c(c(E, ARG), e(ARG)))), e(c(C, c(c(E, ARG), e(ARG))))))))), ARG))), ARG), c(e(e(c(E, ARG))), ARG))

# W = S S (S K)
cW = c(c(e(c(C, c(e(C), c(C, c(c(E, c(C, c(c(E, ARG), e(ARG)))), e(c(C, c(c(E, ARG), e(ARG))))))))), ARG), c(e(c(C, c(e(c(e(c(E, ARG)), ARG)), c(C, c(c(E, ARG), e(ARG)))))), ARG))

namespace = {k: v for k, v in vars().items() if isinstance(v, ob)}
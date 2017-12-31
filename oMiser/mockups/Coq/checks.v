
Require Import Coq.Unicode.Utf8_core.
Require Import primitive_notions.

(* Some simple proofs *)

Lemma A_B_to_Precedence :
  ∀ x y: Ob, (ob_a(x) = x ∧ ob_b(x) = x)  ⇒ x ¶ ob_c(y,x).
Proof.
  intros.
  apply Ob8ThePrecedenceConditionF_floating3.
  apply Ob3Individuals.
  assumption.
Qed.

Lemma TestConsAssociativity :
  ∀ t u y z: Ob, t :: u :: y :: z = t :: (u :: (y :: z)).
Proof.
  trivial.
Qed.

Lemma TestConsAndQuote :
  ` (ob_NIL :: ` ` ob_NIL :: `ob_NIL) = ob_e(ob_c(ob_NIL,ob_c(ob_e(ob_e(ob_NIL)),ob_e(ob_NIL)))).
Proof.
  trivial.
Qed.

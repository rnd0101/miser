
Require Import Coq.Unicode.Utf8_core.
Require Import ob_obap_theory.

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

Definition ob_logo := ob_NIL :: ` ob_NIL.
Definition nob_logo := ` ob_logo.

Lemma ckOb1a :
  ∀ z: Ob, z = (` ob_logo :: ob_NIL) ⇒ (ob_a z = ` ob_logo) ∧ (ob_b z = ob_NIL).
Proof.
  intros.
  apply Ob1PairsA.
  trivial.
Qed.

Eval simpl in ob_a (ob_logo :: ob_b ob_logo).

Lemma ckOb1b :
  ∀ x: Ob, x = ob_a (ob_logo :: ob_b ob_logo) ⇒ x = ob_logo ∧ ob_a x ≠ x ∧ ob_b x ≠ x.
Proof. (* kudos to Anton Trunov https://stackoverflow.com/q/48048374 *)
  unfold ob_logo; intros H.
  rewrite <-Ob1PairsB.
  remember (ob_c (ob_NIL, ob_e ob_NIL)) as f eqn:F.
  pose proof (Ob1PairsA F) as [F1 F2].
  remember (ob_c (f, ob_b f)) as g eqn:G.
  pose proof (Ob1PairsA G) as [G1 G2].
  split; congruence.
Qed.

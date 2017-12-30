
(* Primitive notions *)

(* Some syntactic sugar *)
Require Import Coq.Unicode.Utf8_core.
Notation "x ⇒ y" := (x -> y)
                      (at level 99, y at level 200, right associativity): type_scope.
Notation "x ⇔ y" := (x <-> y) (at level 95, no associativity): type_scope.

Require Export Classical_Prop.
Require Export Classical_Pred_Type.

Axiom excluded_middle: forall P: Prop, P \/ ~P.  (* part of classic? *)

Set Implicit Arguments.

Variable Ob : Type.
Variables ob_a ob_b ob_e : Ob -> Ob.
Variable ob_is_individual ob_is_singleton ob_is_pair ob_is_enclosure: Ob -> Prop.
Variable ob_c : Ob * Ob -> Ob.
Variable prec : Ob * Ob -> Prop.

Notation "x ¶ y" := (prec(x, y)) (at level 70, no associativity): type_scope.


Axiom Ob1PairsA :
    ∀ x y z : Ob, z = ob_c(x,y) ⇒ ob_a(z) = x ∧ ob_b(z) = y.

Axiom Ob1PairsB :
    ∀ x y z : Ob, z = ob_c(ob_a(z),ob_b(z)) ⇔ ob_a(z) ≠ z ∧ ob_b(z) ≠ z.

Axiom Ob2EnclosuresA :
    ∀ x z : Ob, z = ob_e(x) ⇒ ob_a(z) = x ∧ ob_b(z) = z.

Axiom Ob2EnclosuresB :
    ∀ z : Ob, z = ob_e(ob_a(z)) ⇔ ob_a(z) ≠ z ∧ ob_b(z) = z.

Axiom Ob3Individuals :
    ∀ z : Ob, ob_is_individual(z) ⇔ ob_a(z) = z ∧ ob_b(z) = z.

Axiom Ob4StructuralDiscriminationPredicatesA :
        ∀ z : Ob, ob_is_singleton(z) ⇔ ob_b(z) = z.
Axiom Ob4StructuralDiscriminationPredicatesB :
  ∀ z : Ob, ob_is_pair(z) ⇔ ¬ ob_is_singleton(z).
Axiom Ob4StructuralDiscriminationPredicatesC :
  ∀ z : Ob, ob_is_enclosure(z) ⇔ ob_is_singleton(z) ∧ ob_a(z) ≠ z.

Axiom Ob5Totality:
  ∀ z : Ob, ob_is_individual(z) ∨ ob_is_enclosure(z) ∨ ob_is_pair(z).
 
Lemma totality : ∀ z : Ob,
        (ob_is_individual(z) ∧ ¬ ob_is_enclosure(z) ∧ ¬ ob_is_pair(z))
        ∨ (ob_is_enclosure(z) ∧ ¬ ob_is_individual(z) ∧ ¬ ob_is_pair(z))
        ∨ (ob_is_pair(z) ∧ ¬ ob_is_enclosure(z) ∧ ¬ ob_is_individual(z)).            
Proof.
  intros A.
  classical_left.
  intuition.
  (* TODO *)
Admitted.

Axiom Ob6StructuralIdentityA:
         ∀ u v w x y z : Ob, u = ob_c(v,w) ∧ z = ob_c(x,y)
                   ⇒ (u = z ⇔ v = x ∧ w = y).

Axiom Ob6StructuralIdentityB:
        ∀ u v x z : Ob, u = ob_e(v) ∧ z = ob_e(x)
                   ⇒ (u = z ⇔ v = x).

Axiom Ob6StructuralIdentityC:
        ∀ u z : Ob, ob_is_pair(u) ∧ ob_is_singleton(z) ⇒ u ≠ z.

Axiom Ob6StructuralIdentityD:
                     ∀ u z : Ob, ob_is_individual(u) ∧ ob_a(z) ≠ z ⇒ u ≠ z.


Parameter ob_NIL : Ob.

Axiom Ob7IdentityAmongPrimitiveIndividuals :
  ob_is_individual(ob_NIL).

Axiom Ob8ThePrecedenceConditionA_irreflexive :   
  ∀ x : Ob, ¬ (x ¶ x).                                
Axiom Ob8ThePrecedenceConditionB_asymetrical :   
  ∀ x y: Ob, (x ¶ y) ⇒ ¬ (y ¶ x).
Axiom Ob8ThePrecedenceConditionC_transitive :   
  ∀ x y z: Ob, (x ¶ y) ∧ (y ¶ z) ⇒ (x ¶ z).
Axiom Ob8ThePrecedenceConditionD_ordering :   
  ∀ x y: Ob,  x = y ∨ x ¶ y ∨ y ¶ x.

Axiom Ob8ThePrecedenceConditionE_construction :   
  ∀ y z: Ob, z = ob_e(y) ⇔ (y ¶ z).

Axiom Ob8ThePrecedenceConditionE_construction2 :   
  ∀ x y z: Ob, z = ob_c(x,y) ⇔ (x ¶ z) ∧ (y ¶ z).

Axiom Ob8ThePrecedenceConditionF_floating1 :   
  ∀ x: Ob, ob_is_individual(x) ⇒ x ¶ ob_e(x).
                      
Axiom Ob8ThePrecedenceConditionF_floating2 :
  ∀ x y: Ob, ob_is_individual(x) ⇒ x ¶ ob_c(x,y) .     

Axiom Ob8ThePrecedenceConditionF_floating3 :   
   ∀ x y: Ob, ob_is_individual(x) ⇒ x ¶ ob_c(y,x).
        

(* Some simple proofs *)

Lemma A_B_to_Precedence :
  ∀ z y: Ob, (ob_a(z) = z ∧ ob_b(z) = z)  ⇒ z ¶ ob_c(y,z).
Proof.
  intros.
  apply Ob8ThePrecedenceConditionF_floating3.
  apply Ob3Individuals.
  auto.
Qed.


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
Variable obap_is_evref obap_is_evbinop obap_is_evunop: Ob -> Prop.
Variable ob_c : Ob * Ob -> Ob.
Variable prec : Ob * Ob -> Prop.

Notation "x ¶ y" := (prec(x, y)) (at level 70, no associativity): type_scope.

Notation "x :: y" := (ob_c(x,y)) (at level 60, right associativity): type_scope.
Notation "` x" := (ob_e(x)) (at level 55, right associativity).


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
 
Axiom Ob5totality2 :
  ∀ z : Ob,
    (ob_is_individual(z) ∧ ¬ ob_is_enclosure(z) ∧ ¬ ob_is_pair(z))
    ∨ (ob_is_enclosure(z) ∧ ¬ ob_is_individual(z) ∧ ¬ ob_is_pair(z))
    ∨ (ob_is_pair(z) ∧ ¬ ob_is_enclosure(z) ∧ ¬ ob_is_individual(z)).            

Axiom Ob6StructuralIdentityA:
  ∀ u v w x y z : Ob, u = ob_c(v,w) ∧ z = ob_c(x,y)
                   ⇒ (u = z ⇔ v = x ∧ w = y).

Axiom Ob6StructuralIdentityB:
  ∀ u v x z : Ob, u = ob_e(v) ∧ z = ob_e(x) ⇒ (u = z ⇔ v = x).

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

Parameter obap_A : Ob.
Parameter obap_B : Ob.
Parameter obap_C : Ob.
Parameter obap_D : Ob.
Parameter obap_E : Ob.
Parameter obap_SELF : Ob.
Parameter obap_ARG : Ob.
Parameter obap_EV : Ob.

Variable obap_is_primitive: Ob -> Prop.

Axiom PrimitiveIndividualNIL: obap_is_primitive(ob_NIL).
Axiom PrimitiveIndividualA: obap_is_primitive(obap_A).
Axiom PrimitiveIndividualB: obap_is_primitive(obap_B).
Axiom PrimitiveIndividualC: obap_is_primitive(obap_C).
Axiom PrimitiveIndividualD: obap_is_primitive(obap_D).
Axiom PrimitiveIndividualE: obap_is_primitive(obap_E)        .
Axiom PrimitiveIndividualSELF: obap_is_primitive(obap_SELF).
Axiom PrimitiveIndividualARG: obap_is_primitive(obap_ARG).
Axiom PrimitiveIndividualEV: obap_is_primitive(obap_EV).


Variable obap_is_lindy: Ob -> Prop.

(* TODO: String definition *)

Axiom Obap2LiteralIndividualsC:
  ∀ x: Ob, obap_is_lindy(x) ⇒ ob_is_individual(x).

Axiom Obap2LiteralIndividualsD:
  ∀ x y: Ob, obap_is_lindy(x) ∧ ¬ obap_is_lindy(y) ⇒ x ≠ y.

(* Obap3. Universal Apply Function *)
Variable obap_ap: Ob * Ob -> Ob. 
Variable obap_d: Ob * Ob -> Ob. 
Variable obap_apint: Ob * Ob -> Ob. 
Variable obap_ev: Ob * Ob * Ob -> Ob. 
Variable obap_eval: Ob -> Ob. 
Variable obap_is_pure_lindy: Ob -> Prop.
Variable obap_is_lindy_everywhere: Ob -> Prop.

Axiom Obap4apA:
  ∀ x: Ob, obap_is_lindy(x) ⇒ obap_is_pure_lindy(x).
Axiom Obap4apB:
  ∀ x y: Ob, obap_is_pure_lindy(x :: y) ⇔ obap_is_pure_lindy(x) ∧ obap_is_pure_lindy(y).
Axiom Obap4apC:
  ∀ x: Ob, ¬ obap_is_pure_lindy(ob_e(x)).

Axiom Obap4apD:
  ∀ x: Ob, obap_is_lindy(x) ⇒ obap_is_lindy_everywhere(x).
Axiom Obap4apE:
  ∀ x: Ob, obap_is_lindy_everywhere(ob_e(x)) ⇔ obap_is_lindy_everywhere(x).
Axiom Obap4apF:
  ∀ x y: Ob, obap_is_lindy_everywhere(x :: y)
             ⇔ obap_is_lindy_everywhere(x) ∧ obap_is_lindy_everywhere(y).

Axiom Obap4apG:
  ∀ p x: Ob, ob_is_enclosure(p) ⇒ obap_ap(p,x) = ob_a(p).

Axiom Obap4apH:
  ∀ p x: Ob, ob_is_individual(p) ⇒ obap_ap(p,x) = obap_apint(p,x).

Axiom Obap4apI:
  ∀ p x: Ob, obap_is_pure_lindy(p) ∧ obap_is_lindy_everywhere(x)
        ⇒ (ob_is_pair(p) ⇒ obap_ap(p,x) = p :: x).                                     

Axiom Obap4apJ:
  ∀ p x: Ob, ¬ ( obap_is_pure_lindy(p) ∧ obap_is_lindy_everywhere(x) )
        ⇒ (ob_is_pair(p) ⇒ obap_ap(p,x) = obap_ev(p,x,p)).

Axiom Obap5ApplicativeTreatmentOfIndividualsA:   
  ∀ x: Ob, obap_apint(ob_NIL, x) = x.
Axiom Obap5ApplicativeTreatmentOfIndividualsB:
  ∀ x: Ob, obap_apint(obap_A, x) = ob_a(x).
Axiom Obap5ApplicativeTreatmentOfIndividualsC:   
  ∀ x: Ob, obap_apint(obap_B, x) = ob_b(x).
Axiom Obap5ApplicativeTreatmentOfIndividualsD:   
  ∀ x: Ob, obap_apint(obap_C, x) = obap_C :: ob_e(x) :: obap_ARG.
Axiom Obap5ApplicativeTreatmentOfIndividualsE:
  ∀ x: Ob, obap_apint(obap_D, x) = obap_D :: ob_e(x) :: obap_ARG.
Axiom Obap5ApplicativeTreatmentOfIndividualsF:
  ∀ x: Ob, obap_apint(obap_E, x) = ob_e(x).
Axiom Obap5ApplicativeTreatmentOfIndividualsG:    
  ∀ x: Ob, obap_apint(obap_SELF, x) = ob_e(obap_SELF) :: ob_e(x).
Axiom Obap5ApplicativeTreatmentOfIndividualsH:
  ∀ x: Ob, obap_apint(obap_ARG, x) = ob_e(obap_ARG) :: ob_e(x).
Axiom Obap5ApplicativeTreatmentOfIndividualsI:
  ∀ x: Ob, obap_apint(obap_EV, x) = ob_e(obap_EV) :: ob_e(x).  
Axiom Obap5ApplicativeTreatmentOfIndividualsJ:
  ∀ p x: Ob, obap_is_lindy(p) ∧ obap_is_lindy_everywhere(x)
     ⇒ obap_apint(p,x) = p :: x.
Axiom Obap5ApplicativeTreatmentOfIndividualsK:
  ∀ p x: Ob, obap_is_lindy(p) ∧ ¬ obap_is_lindy_everywhere(x)  
     ⇒ obap_apint(p,x) = p :: ob_e(x).

(* Evaluation functions *)
Axiom Obap6EvA:
  obap_is_evref(obap_SELF).
Axiom Obap6EvB:   
  obap_is_evref(obap_ARG).
Axiom Obap6EvC:        
  ∀ p x: Ob, obap_ev(p,x,obap_SELF) = p.
Axiom Obap6EvD:
  ∀ p x: Ob, obap_ev(p,x,obap_ARG) = x.
Axiom Obap6EvE:        
  ∀ e p x: Ob, ob_is_individual(e) ∧ ¬ obap_is_evref(e) ⇒ obap_ev(p,x,e) = e.
Axiom Obap6EvF:   
  ∀ p x y : Ob, obap_ev(p,x,ob_e(y)) = y.
Axiom Obap6EvG:
  obap_is_evbinop(obap_C).
Axiom Obap6EvH:
  obap_is_evbinop(obap_D).
Axiom Obap6EvI:   
  ∀ e1 e2 p x: Ob, obap_ev(p,x,obap_C::e1::e2) = ob_c(obap_ev(p,x,e1), obap_ev(p,x,e2)).
Axiom Obap6EvJ:          
  ∀ e1 e2 p x: Ob, obap_ev(p,x,obap_D::e1::e2) = obap_d(obap_ev(p,x,e1), obap_ev(p,x,e2))       .
Axiom Obap6EvK:
  ∀ x y: Ob, x = y ⇒ obap_d(x,y) = obap_A.
Axiom Obap6EvL:
  ∀ x y: Ob, x ≠ y ⇒ obap_d(x,y) = obap_B.
Axiom Obap6EvM:
  ∀ e1 e2 p x: Ob, obap_is_evbinop(e1) ∧ ob_is_singleton(e2)
     ⇒ obap_ev(p,x,e1::e2) = obap_ap(e1, obap_ev(p,x,e2)).
Axiom Obap6EvN:   
  obap_is_evunop(obap_EV).
Axiom Obap6EvO:   
  ∀ e2 p x: Ob, obap_ev(p,x,obap_EV :: e2) = obap_ev(p,x,obap_ev(p,x,e2)).
Axiom Obap6EvP:
  ∀ e1 e2 p x: Ob, ¬ ( obap_is_evbinop(e1) ∨ obap_is_evunop(e1) )
           ⇒ obap_ev(p,x,e1::e2) = obap_ap(obap_ev(p,x,e1), obap_ev(p,x,e2)).

Axiom Obap7Eval:
  ∀ e: Ob, obap_eval(e) = obap_ev(obap_SELF, obap_ARG, e).
                                

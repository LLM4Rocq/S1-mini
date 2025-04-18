From mathcomp Require Import ssreflect ssrfun ssrbool ssrnat.

Set Implicit Arguments.
Unset Strict Implicit.
Unset Printing Implicit Defensive.

Lemma test_dup1 : forall n : nat, odd n.
Proof. move=> /[dup] m n; suff: odd n by []. Abort.

Lemma test_dup2 : let n := 1 in False.
Proof. move=> /[dup] m n; have : m = n := erefl. Abort.

Lemma test_swap1 : forall (n : nat) (b : bool), odd n = b.
Proof. move=> /[swap] b n; suff: odd n = b by []. Abort.

Lemma test_swap1 : let n := 1 in let b := true in False.
Proof. move=> /[swap] b n; have : odd n = b := erefl. Abort.

Lemma test_apply A B : forall (f : A -> B) (a : A), False.
Proof.
move=> /[apply] b.
Check (b : B).
Abort.

Lemma test_swap_plus P Q : P -> Q -> False.
Proof.
move=> + /[dup] q.
suff: P -> Q -> False by [].
Abort.

Lemma test_dup_plus2 P : P -> let x := 0 in False.
Proof.
move=> + /[dup] y.
suff: P -> let x := 0 in False by [].
Abort.

Lemma test_swap_plus P Q R : P -> Q -> R -> False.
Proof.
move=> + /[swap].
suff: P -> R -> Q -> False by [].
Abort.

Lemma test_swap_plus2 P : P -> let x := 0 in let y := 1 in False.
Proof.
move=> + /[swap].
suff: P -> let y := 1 in let x := 0 in False by [].
Abort.

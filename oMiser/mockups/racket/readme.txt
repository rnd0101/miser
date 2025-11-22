oFrugal / oMiser — Local Development Setup (Plain Text)
=======================================================

This project contains two Racket collections:

  • omiser/   – runtime for ob / c / e / ap / ev / eval
  • oFrugal/  – #lang oFrugal reader + module-begin

Everything is installed in *development (linked) mode*, so Racket
loads your source files directly — no copying.


0. Requirements
---------------
Racket 8.18 or later.



1. Directory Layout (expected)
------------------------------
Your repo root should look like this:

  repo-root/
    info.rkt                  <-- root (multi-collection) info
    omiser/
      info.rkt
      runtime.rkt
    oFrugal/
      info.rkt
      lang/
        reader.rkt
        module-begin.rkt
    demo.ofrugal



2. Required info.rkt Files
--------------------------

(2.1) repo-root/info.rkt
-------------------------
#lang info
(define collection 'multi)
(define deps '("base"))
(define version "0.0.1")
(define pkg-desc "oFrugal language + oMiser runtime")

This tells Racket the package contains multiple collections.


(2.2) omiser/info.rkt
----------------------
#lang info
(define collection "omiser")
(define deps '("base"))
(define version "0.0.1")


(2.3) oFrugal/info.rkt
-----------------------
#lang info
(define collection "oFrugal")
(define deps '("base"))
(define version "0.0.1")



3. Install the Package (development link)
-----------------------------------------

IMPORTANT: You must run raco from the repo root — the directory
that contains the root info.rkt.

Commands:

  cd /path/to/repo-root
  raco pkg install

This installs the entire directory as a linked package
(i.e., no copying of files).

Alternative explicit install:

  raco pkg install --link . --name oFrugal-multi

(but normally just “raco pkg install” is correct when run
in the directory containing info.rkt.)



4. Build/Compile the Collections
--------------------------------

After installation, build both collections:

  raco setup -D oFrugal omiser

(-D skips docs for speed.)

If you see errors, check that all info.rkt files exist.



5. Running Files
----------------

Example file: demo.ofrugal

  #lang oFrugal

  ob ^x = `foo :: `bar :: .NIL;
  (.D ^x ^x);
  ^x

Run:

  racket demo.ofrugal



6. Development Workflow
-----------------------

Because the package is **linked**, normal code edits do NOT
require reinstallation.

Just rerun:

  racket demo.ofrugal

Racket automatically recompiles changed modules.


When you change the language reader or macros:
----------------------------------------------
Force rebuild:

  raco setup -D oFrugal


When you modify info.rkt or change layout:
------------------------------------------
Update metadata, then rebuild:

  raco pkg update
  raco setup -D oFrugal omiser


If compiled artifacts become corrupted:
---------------------------------------
  raco setup --clean oFrugal
  raco setup -D oFrugal



7. Uninstall
------------
  raco pkg remove oFrugal

(Use “raco pkg show” to find the installed name.)


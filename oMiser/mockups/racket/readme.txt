oFrugal / oMiser — Development Setup
====================================

Project purpose
---------------
This repository provides a Racket implementation of the **oMiser computational model**
and the **oFrugal language** (a surface syntax for expressing ob-expressions).

For theory, reference documentation, and background materials, see:

    https://orcmid.github.io/miser/

This includes the ob model, CFob canonical forms, Frugalese grammar,
and the broader Miser computational framework.


Development installation
------------------------
Install the repository as a *linked* Racket package (no copying):

  raco pkg install

Run this from the repository root (the directory containing info.rkt).

This makes Racket load your local source files directly, so edits are
immediately reflected.


Rebuilding after changes
------------------------
When you change interpreter/runtime or language reader code:

  raco setup -D oFrugal omiser

When changing only the oFrugal reader:

  raco setup -D oFrugal

When metadata or directory layout changes:

  raco pkg update
  raco setup -D oFrugal omiser


Uninstall
---------
To remove the package:

  raco pkg remove oFrugal

You can inspect installed package names with:

  raco pkg show


Running .ofrugal programs
-------------------------
An oFrugal file begins with:

  #lang oFrugal

Run any such file with:

  racket your-file.ofrugal

Example:

  racket demo.ofrugal

Any top-level expression producing an ob value will be displayed in CFob form.

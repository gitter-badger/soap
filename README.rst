====
SOAP
====

**SOAP** is a tool for automatically exploring optimisations to a numerical C
program, so that when it is synthesized into an FPGA implementation, the error,
area, and latency of the implementation are minimised.


Installation
============

Requirements:
* Python3

::

  $ pip install -r requirements.txt



Usage
=====

::

  ./soapy --help



Benchmark Results
=================

Available here_.

.. _here: https://admk.github.io/soap/plot.html


Caveat
======

The tool is still in its early stage, so please expect many rough edges and
bugs.  Please feel free to file an issue when you encounter a bug.


.. image:: https://badges.gitter.im/admk/soap.svg
   :alt: Join the chat at https://gitter.im/admk/soap
   :target: https://gitter.im/admk/soap?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
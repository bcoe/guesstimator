Sampy
=====

Sampy estimates the number of times an operation occurs in a distributed system:

* It's backed by Redis.
* It's meant to be simple; pretty much all you get is an increment operation.
* It performs writes probabilistically, providing only an estimate of the number of times an operation has occurred.

Usage
-----
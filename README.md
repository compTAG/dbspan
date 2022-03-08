# DBSpan

This repo is a quick and dirty implementation of the DBSpan algorithm.

## Getting started

I assume that you are working on a unix based system such as OS X or Ubuntu and
have installed

- python
- mini conda

I recommend setting up an environment with conda and install pip

	conda create --name dbspan python=3.10 pip

Activate the environment

    conda activate dbspan

Run the tests with

    make test

When you want to clean up

    conda deactivate
    conda remove -n dbspan --all

#!/bin/bash

export VIRTUAL_ENV="./venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME

if [ ! -d ./venv ]
then
    virtualenv venv
fi

if [ ! -d ./venv/lib/python2.7/site-packages/flask ]
then
    pip install -r requirements.txt
fi

COV=$(ls bblogger/*.py | sed "s/^/--cov=/" | sed "s/\.py$//" | \
	sed "s#/__init__##" | sed "s#/#.#" | tr "\n" " ")
pep8 *.py tests/*.py && pylint *.py tests/*.py && \
	PYTHONPATH=. py.test -v $COV --cov-report=term-missing tests

#!/bin/bash

if [ -n "$(command -v yum)" ]; then
	echo "yum"
else
	if [ -n "$(command -v apt-get)" ]; then
		echo "apt"
	else
		if [ -n "$(command -v brew)" ]; then
			echo "brew"
		else
			echo "No package installer found"
		fi
	fi
fi

python setup.py sdist
python setup.py install
grapher
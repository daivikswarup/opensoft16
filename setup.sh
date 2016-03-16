#!/bin/bash

apt_packages=( build-essential python-dev python-pip tesseract-ocr tesseract-ocr-eng libopencv-dev)

function installer {
	echo "Installing packages using $1"
	# cycle through the package list to install packages
	for item in ${apt_packages[*]}
	do
		apt-get install $item
    done
}

installer
python setup.py sdist
python setup.py install
grapher
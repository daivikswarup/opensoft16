#!/bin/bash

yum_packages=()
apt_packages=()
brew_packages=(opencv sip poppler)

function install_package {
	# install package using command for the available package installer
	if [ "$1" == "brew" ]; then
		$1 install $2
    fi

    if [ "$1" == "apt" ]; then
		apt-get install $2
    fi

    if [ "$1" == "yum" ]; then
		$1 install $2
    fi
}

function installer {
	echo "Installing packages using $1"
	# cycle through the package list to install packages
	for item in ${brew_packages[*]}
	do
		install_package $1 $item
    done
}

function install_required {
	# check which package manager we have
	if [ -n "$(command -v yum)" ]; then
		echo "yum"
		installer "yum"
	else
		if [ -n "$(command -v apt-get)" ]; then
			echo "apt"
			installer "apt"
		else
			if [ -n "$(command -v brew)" ]; then
				echo "brew"
				installer "brew"
			else
				echo "No package installer found"
			fi
		fi
	fi
}

install_required
python setup.py sdist
python setup.py install
grapher
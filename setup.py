from setuptools import setup

setup(
    # Application name:
    name="Grapher",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Akshay Gupta",
    author_email="akshaysngupta@gamil.com",

    # Packages
    packages=["Grapher"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/Grapher/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "pytesseract",
        "matplotlib",
        "scipy",
        "numpy",
        "wxpython",
    ],
    entry_points={
        'console_scripts': [
            'grapher = Grapher.run:main',
        ],
    },
)
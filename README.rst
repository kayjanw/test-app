***************************************
utils.py Project
***************************************

.. image:: https://readthedocs.org/projects/kayjan/badge/?version=latest
   :target: https://kayjan.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

This ``utils.py`` project aims to be a helper tool to automate repetitive data analysis tasks,
or perform predictions and optimizations that are computationally expensive etc.
This documentation comprises of deployment documentation and code documentation.


File Structure
========================
This project aims to follow software engineering best practices and has the following file structure.
There are many other ways to structure your codes, but I find this implementation easiest for me.

::

  project
  ├── assets
  │   ├── default_css.css
  │   └── etc (other .css, .ico, .png, .svg files)
  ├── components
  │   ├── helper.py
  │   └── etc (other .py files)
  ├── data
  │   ├── model.pkl
  │   └── etc (other .pkl files)
  ├── docs
  │   ├── build
  │   ├── source
  │   ├── make.bat
  │   └── Makefile
  ├── app.py
  ├── callbacks.py
  ├── layouts.py
  ├── requirements.txt
  └── routes.py

Project's file structure has the following dependency diagram

.. image:: ../../assets/file-dependency.png
  :alt: Dependency Diagram
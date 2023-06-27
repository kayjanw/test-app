***************************************
utils.py Project
***************************************

.. image:: https://readthedocs.org/projects/kayjan/badge/?version=latest
   :target: https://kayjan.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

This ``utils.py`` project aims to be a helper tool to automate repetitive data analysis tasks,
perform predictions and optimizations that are computationally expensive, and play games.
This documentation comprises of deployment documentation and code documentation.

The web application can be found `here <https://kayjan.fly.dev>`_.


File Structure
========================
This project aims to follow software engineering best practices and has the following file structure.
There are many other ways to structure your codes, but I find this implementation easiest for me.

::

  project
  ├── assets
  │   ├── default_css.css
  │   └── etc (other .css, .ico, .png, .svg files)
  ├── callbacks
  │   ├── callbacks.py
  │   ├── trip_planner.py
  │   └── etc (other callback .py files for each tab)
  ├── components
  │   ├── helper.py
  │   ├── trip_planner.py
  │   └── etc (other python classes .py files)
  ├── data
  │   ├── model.pkl
  │   └── etc (other .pkl/.xlsx data files)
  ├── docs
  │   ├── build
  │   ├── source
  │   ├── make.bat
  │   └── Makefile
  ├── layouts
  │   ├── articles.py
  │   └── etc (other layout .py files for each tab)
  ├── tests
  ├── app.py
  ├── pyproject.toml
  ├── requirements.txt
  └── routes.py

Project's file structure has the following dependency diagram

.. image:: ../../assets/file-dependency.png
  :alt: Dependency Diagram

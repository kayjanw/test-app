***************************************
Creating Virtual Environment
***************************************

During deployment, it is always recommended to create a virtual environment simulating the deployment environment.
Running application on virtual environment helps to check if there are are any missing package or conflicting
package versions.

.. note:: The following instructions are tested on Windows

Creating VE using Anaconda
--------------------------

This is the recommended way to create and manage your virtual environments.
Virtual environments can be created on conda command line with

::

    conda create -n environment_name python=3.6

Virtual environment only needs to be created once, to view the full list of virtual environments and their locations

::

    conda env list

The following lines can activate, deactivate and delete the created virtual environment

::

    conda activate environment_name
    conda deactivate
    conda env remove --name environment_name


Creating VE using Shell Command
-------------------------------

Virtual environments can be created on command line with

::

    python -m venv environment_name

The following lines can activate, deactivate and delete the created virtual environment

::

    source environment_name/Scripts/activate
    deactivate
    rm -r environment_name/


Creating VE using Python Code
-------------------------------

Virtual environments can be created using Python code by

.. code:: Python

    import venv
    venv.create("environment_name")

Activation, deactivation and deletion of created virtual environment is done via the shell command, same as above.

***************************************
Creating Virtual Environment
***************************************

During deployment, it is always recommended to create a virtual environment simulating the deployment environment.
Running application on virtual environment helps to check if there are are any missing package or conflicting
package versions.


Creating VE using Anaconda
--------------------------

Virtual environments can be created on conda command line with::

    conda create -n environment_name python=3.6

Virtual environment only needs to be created once, to view the full list of virtual environments and their locations::

    conda info --envs

The following lines can activate or deactivate the created virtual environment::

    conda activate environment_name
    conda deactivate


Creating VE using Shell Command
-------------------------------

The following codes are instructions I have picked up from e-learning courses and are not tested.
Virtual environments can be created on command line with::

    python -m venv .venv


The following lines can activate the created virtual environment::

    source .venv/bin/activate


Creating VE using Python Code
-------------------------------

The following codes are instructions I have picked up from e-learning courses and are not tested.
Virtual environments can be created using Python code by

.. code:: Python

    import venv
    venv.create(".venv")

import os
import setuptools
from setuptools.config import read_configuration

cfg_dict = read_configuration("setup.cfg")

try:
    print("checking for cython")
    # if cython is installed, use it to compile
    from Cython.Build import cythonize

    ext_mods = [setuptools.Extension("simpletree3.algorithms",
            [
                "simpletree3/algorithms.py"
            ]),
            setuptools.Extension("simpletree3.nodes",
            [
                "simpletree3/nodes.py"
            ])
            ]
    setuptools.setup(
        ext_modules=cythonize(ext_mods),
        **cfg_dict["metadata"]
    )

except Exception as e_:
    # no cython, or error compiling
    # fall back to pure python
    print("building pure python")
    setuptools.setup(
        **cfg_dict["metadata"]
    )

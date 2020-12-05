# This setup.py file is just needed to support editable installs
from setuptools import setup
setup(
    use_scm_version={
        "write_to": "ordest/_version.py",
        "version_scheme": "post-release",
    },
    setup_requires=['setuptools_scm']
)

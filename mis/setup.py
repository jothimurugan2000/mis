from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mis/__init__.py
from mis import __version__ as version

setup(
	name="mis",
	version=version,
	description="Management Reporting",
	author="B & K Securities",
	author_email="naveen.prabhu@bksec.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

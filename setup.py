from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in supplementary_invoice/__init__.py
from supplementary_invoice import __version__ as version

setup(
	name="supplementary_invoice",
	version=version,
	description="This app used to change rate on sale sinvoice",
	author="Quantbit",
	author_email="abhishekshinde9503@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

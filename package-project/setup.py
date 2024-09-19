from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="jd-image-processing",
    version="0.0.1",
    author="judenilson",
    author_email="judenilson@hotmail.com",
    description="Image Processing",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Judenilson/dio-python-bootcamp/tree/main/package-project",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
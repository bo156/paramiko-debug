from setuptools import setup, find_packages

dev_requires = [
    "pytest",
    "tox",
    "flake8",
]

setup(
    name="paramiko_client",
    packages=find_packages(),
    requires=["paramiko", "six"],
    extras_require={"dev": dev_requires},
    version="0.0.1",
)

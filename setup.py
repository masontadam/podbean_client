from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="podbean_client",
    version="0.0.0",
    description="A Python client library for the Podbean API!",
    py_modules=["podbean_client"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/masontadam/podbean_client",
    author="Mason Adam",
    author_email="masontadam@gmail.com",

    install_requires = [
        "requests_oauthlib",
        "requests"
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
        ],
    },
)

from setuptools import setup

def readme():
    with open("README.rst", "r") as fh:
        return fh.read()

setup(
    name="podbean_client",
    version="1.0.1",
    description="A Python client library for the Podbean API!",
    py_modules=["podbean_client"],
    package_dir={"": "src"},
    long_description=readme(),
    long_description_content_type="text/x-rst",
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
            "Flask",
            "python-dotenv"
        ],
    },
)

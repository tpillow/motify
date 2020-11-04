# Imports
import setuptools

# Read README file
with open("README.md", "r") as fh:
    longDescription = fh.read()

# Configure setup
setuptools.setup(
    name="motify-tpillow",
    version="0.0.1",
    author="tpillow",
    author_email="hesosas765@wpfoo.com",
    description="A small, lightweight cross-platform notification system.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/tpillow/motify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)

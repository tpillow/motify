# Imports
import setuptools

# Long description MD format
longDescription: str = """# Motify

## A small, lightweight cross-platform notification system.

Just need to show a notification to the user on any OS? Don't want the native notifications with flaky abilities? Use Motify.
"""

# Configure setup
setuptools.setup(
    name="motify-tpillow",
    version="0.0.2",
    author="tpillow",
    author_email="hesosas765@wpfoo.com",
    description="A small, lightweight cross-platform notification system.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    license="LICENSE.txt",
    url="https://github.com/tpillow/motify",
    packages=["motify"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)

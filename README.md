# Motify (Incomplete Project)

## A small, lightweight cross-platform notification system.

Just need to show a notification to the user on any OS? Don't want the native notifications with flaky abilities? Use Motify.

## Developer Resources

Motify uses tkinter, which comes installed with Python 3.

To test the package while developing, run `pip install .` from the root git directory. This will install motify as it is in the `motify` source folder.

### PyPi Info

Just some notes so I remember how to package this up and submit it to PyPi :)

```
py -3 setup.py sdist bdist_wheel
py -3 -m twine upload --repository testpypi dist/*
Use __token__ as username. Token as password.

pip install --index-url https://test.pypi.org/simple/ --no-deps motify-tpillow
```

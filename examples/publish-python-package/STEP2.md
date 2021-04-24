# Set up pypi

Create a file in the home directory called `~/.pypirc` with contents:

```text
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = YourPyPiUsername
password = YourPyPiPassword

[testpypi]
repository = https://test.pypi.org/legacy/
username = YourPyPiUsername
password = YourPyPiPassword
```

For better security, execute `chmod 600 ~/.pypirc`

> :warning: Instead of using the password field, consider saving your API tokens and passwords securely using keyring (which is installed by Twine):
>  
> ```bash
> keyring set https://upload.pypi.org/legacy/ __token__
> keyring set https://test.pypi.org/legacy/ __token__
> keyring set <private-repository URL> <private-repository username>
> ```

## Build, register, and upload to PyPi

Open terminal window and change directory to /project/

Then run setup.py with `sdist` to build a source distribution and `bdist_wheel` to build a wheel. Then use twine to register it and upload to pypi.

```shell
python3 setup.py sdist bdist_wheel
twine check dist/*

# For test / pre-release
twine upload -r testpypi dist/*

# For production
twine upload -r pypi dist/*
```

## Build and upload subsequent updates to PyPi

Update the change log and edit the version number in `setup.py`

```shell
rm dist/*
python3 setup.py sdist bdist_wheel
twine check dist/*

# For test / pre-release
twine upload -r testpypi dist/*

# For production
twine upload -r pypi dist/*
```

---

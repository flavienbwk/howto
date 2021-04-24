# To distribute a package on pypi

## Directory structure

```text
/project
    /mymodule
        __init__.py
        module.py
    setup.py
```

## File contents

### /project/package/\_\_init\_\_.py

```python
import pkg_resources
from .module import *
version = pkg_resources.require("mymodule")[0].version
```

### /project/package/module.py

```python
# this file just contains your module's code
```

### /project/setup.py

```python
from setuptools import setup
setup(name='mymodule',
      version='0.1',
      description='What the module does',
      url='https://github.com/username/repo',
      author='Your Name',
      author_email='email@domain.net',
      license='MIT',
      packages=['mymodule'],
      install_requires=['numpy>=1.11',
                        'matplotlib>=1.5'])
```

-------

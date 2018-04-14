# NotImportChecker
Python module used on editors to check if a imported module is installed.

# Examples
## Test file
### test1.py
```python
import os

print(os.listdir('.'))

```

```python
>>> from notimportchecker import *
>>> c = Checker('test1.py')
>>> c
<notimportchecker.Checker object at 0x7f172352bdd0>
>>> c.get_imports()
{'os': {'lineno': 1, 'mod_name': {'os': 'os'}}}
>>> c.get_not_imports_on_file(c.get_imports())
>>> c._import_error_list
{}
```
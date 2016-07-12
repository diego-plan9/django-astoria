# django-astoria
Utilities for storing and retrieving an AST tree into/from a Django database.

## Introduction

`django-astoria` is a django module for storing and retrieving Python
[Abstract Syntax Trees](https://docs.python.org/2/library/ast.html) into a
Django database (currently only PostgreSQL with `django-lsapling` is supported).

### Example

```python
>>> EXAMPLE = '''
def last(a):
    print a[:-1]
'''

>>> ast_tree = ast.parse(EXAMPLE)
>>> root = AstoriaNode.objects.create_from_ast(ast_tree)
>>> ast.dump(root.as_ast()) == ast.dump(ast_tree)
True

>>> root.pretty_print()
└───[ body*=FunctionDef]
    ├───[@name=last]
    ├───[ args=arguments]
    │   ├───[ args*=Name]
    │   │   ├───[@id=a]
    │   │   └───[ ctx=Param]
    │   ├───[@vararg=None]
    │   ├───[@kwarg=None]
    │   └───[@defaults=[]]
    ├───[ body*=Print]
    │   ├───[@dest=None]
    │   ├───[ values*=Subscript]
    │   │   ├───[ value=Name]
    │   │   │   ├───[@id=a]
    │   │   │   └───[ ctx=Load]
    │   │   ├───[ slice=Slice]
    │   │   │   ├───[@lower=None]
    │   │   │   ├───[ upper=Num]
    │   │   │   │   └───[@n=-1]
    │   │   │   └───[@step=None]
    │   │   └───[ ctx=Load]
    │   └───[@nl=True]
    └───[@decorator_list=[]]


```

## Requirements
* Django 1.8
* [django-lsapling](https://github.com/diego-plan9/django-lsapling)
* PostgreSQL

## Known issues

This module is still in alpha state. Notable issues include:
* Support for Django > 1.8 and Python 3.x has not been tested.
* The module requires a library that provides an ordered tree DB implementation.
Currently only `django-lsapling` is supported, but support for other widely used
libraries (`django-treebeard`, `django-mptt`, etc) is planned.

## Changelog

### 0.1.0 (2016/07/11):
* Initial public release.

## License

MIT license, Copyright (c) 2016 Diego M. Rodríguez.


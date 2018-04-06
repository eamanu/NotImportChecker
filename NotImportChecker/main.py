# -*- coding: utf-8 -*-
# GNU General Public License v3

import ast


class SearchImport(ast.NodeVisitor):
    def __init__(self):
        self._imports = {}

    def get_imports(self):
        return self._imports

    def visit_ImportFrom(self, stmt):
        module_name = stmt.module
        names = stmt.names
        names_dict = {}

        for al in names:
            if al.name == '*':
                continue
            names_dict[al.name] = al.name

        self._imports.setdefault(module_name, {'mod_name': names_dict,
                                               'lineno': stmt.lineno})
        for child in ast.iter_child_nodes(stmt):
            self.generic_visit(child)

    def visit_Import(self, stmt):
        for al in stmt.names:
            self._imports.setdefault(al.name, {'mod_name':
                                               {al.name: al.name},
                                               'lineno': stmt.lineno})
        for child in ast.iter_child_nodes(stmt):
            self.generic_visit(child)


class Checker(object):
    def __init__(self, path):
        self._path = path
        self._imports = dict()

    def parse_file(self, path):
        """Parse the file

        Params
        ------
        path: string -- path of the file

        Return
        ------
        stmt: string -- the parse file

        Error:

        -10 -> if there are some problem while try to open the file
        -11 -> syntax error on parse file
        """
        stmt = ''
        try:
            with open(path, 'r') as f:
                stmt = ast.parse(f.read())
            return stmt
        except IOError as ioerror:
            print('{}: Error while try to open the file'.format(str(ioerror)))
            return (-10)
        except SyntaxError as syntaxerror:
            print('{}: Wrong Syntax'.format(str(syntaxerror)))
            return (-11)

    def get_imports(self, path):
        """Return Imports on path

        Params
        ------
        path: string -- path of the file

        Return
        ------
        stmt: dict -- dict of imports and importFrom

        Error
        -----
        -1 -> if there are some problems
        """
        stmt = self.parse_file(path)
        if stmt != -10 or stmt != -11:
            searcher = SearchImport()
            searcher.visit(stmt)
            self._imports = searcher.get_imports()
            return stmt
        return (-1)

    def get_not_imports_on_file(self):



a = SearchImport()
tree = ast.parse('''
from numpy import (array,hola)
import sys
from numpy import vector
from ninja_ide.gui.core.saraza import hello as h
import os
''')
a.visit(tree)

print(a.get_imports())
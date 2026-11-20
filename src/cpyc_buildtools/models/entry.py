import ast
from hashlib import md5
import os
from typing import TypedDict

from cpyc_buildtools.models.util import sanitize

class EntrySpec(TypedDict):
    title: str
    path: str
    description: str
    source: str

class Entry:
    def __init__(self, spec: EntrySpec, section_path: str, *, minimal: bool = False) -> None:
        self.title: str = spec['title']

        path = os.path.join(section_path, spec['path'])
        with open(os.path.join(path, spec['source']), 'r', encoding='utf8') as f:
            self.source = sanitize(f.read())

        if not minimal:
            with open(os.path.join(path, spec['description']), 'r', encoding='utf-8') as f:
                self.description = sanitize(f.read())
        else:
            self.description = ''
        source_ast = ast.parse(self.source)
        ast_str = sanitize(ast.dump(source_ast, indent=4) + '\n')
        self.hash = md5(ast_str.encode('utf-8')).hexdigest()[:8]

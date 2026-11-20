import os
from typing import TypedDict

from cpyc_buildtools.models.entry import Entry, EntrySpec
from cpyc_buildtools.models.util import sanitize

class SectionSpec(TypedDict):
    title: str
    path: str
    description: str
    entries: list[EntrySpec]

class Section:
    def __init__(self, spec: SectionSpec, document_path: str, *, minimal: bool = False) -> None:
        self.title: str = spec['title']

        path = os.path.join(document_path, spec['path'])
        if not minimal:
            with open(os.path.join(path, spec['description']), 'r', encoding='utf-8') as f:
                self.description = sanitize(f.read())
        else:
            self.description = ''
        self.entries: list[Entry] = [
            Entry(entry, path, minimal=minimal)
            for entry in spec['entries']
        ]

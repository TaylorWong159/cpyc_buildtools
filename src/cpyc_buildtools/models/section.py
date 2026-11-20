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
    def __init__(self, spec: SectionSpec, document_path: str) -> None:
        self.title: str = spec['title']
        self.path: str = os.path.join(document_path, spec['path'])
        with open(os.path.join(self.path, spec['description']), 'r', encoding='utf-8') as f:
            self.description = sanitize(f.read())
        self.entries: list[Entry] = [
            Entry(entry, self.path)
            for entry in spec['entries']
        ]

from typing import TypedDict

from cpyc_buildtools.models.section import Section, SectionSpec

class DocumentSpec(TypedDict):
    title: str
    authors: list[str]
    path: str
    sections: list[SectionSpec]

class Document:
    def __init__(self, spec: DocumentSpec, *, minimal: bool = False) -> None:
        self.title: str = spec['title']
        self.authors: str = ', '.join(spec['authors'])
        self.sections: list[Section] = [
            Section(entry, spec['path'], minimal=minimal)
            for entry in spec['sections']
        ]

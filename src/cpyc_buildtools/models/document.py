from typing import TypedDict

from cpyc_buildtools.models.section import Section, SectionSpec

class DocumentSpec(TypedDict):
    title: str
    authors: list[str]
    path: str
    sections: list[SectionSpec]

class Document:
    def __init__(self, spec: DocumentSpec) -> None:
        self.title: str = spec['title']
        self.authors: str = ', '.join(spec['authors'])
        self.path: str = spec['path']
        self.sections: list[Section] = [
            Section(entry, self.path)
            for entry in spec['sections']
        ]

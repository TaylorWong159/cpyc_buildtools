import argparse
from importlib import resources
import json
from typing import NamedTuple

from cpyc_buildtools.models import Document
from cpyc_buildtools.pdfgen import PDFGenerator

TEMPLATES = resources.files('cpyc_buildtools').joinpath('templates')

class Args(NamedTuple):
    document: str
    build: str
    minimal: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'document',
        type=str,
        help='The json document file to build'
    )
    parser.add_argument(
        '-b', '--build',
        type=str,
        default='build',
        help='Path to the directory to put the build artifacts'
    )
    parser.add_argument(
        '-m', '--minimal',
        action='store_true',
        help='Build the minimized version'
    )
    args = parser.parse_args()
    return Args(args.document, args.build, args.minimal)

def build(doc_file: str, build: str = 'build', minimal: bool = False) -> None:
    with open(doc_file, 'r', encoding='utf8') as f:
        doc = Document(json.load(f), minimal=minimal)
    with resources.as_file(TEMPLATES) as templates:
        generator = PDFGenerator(template_dir=str(templates), output_dir=build)
    generator.build_document(doc)


def main() -> None:
    build(*parse_args())

if __name__ == '__main__':
    main()
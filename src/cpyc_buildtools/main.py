import argparse
from importlib import resources
import json
import logging
import os
import sys
from typing import NamedTuple

from cpyc_buildtools.models import Document
from cpyc_buildtools.pdfgen import PDFGenerator

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    force=True
)

TEMPLATES = resources.files('cpyc_buildtools').joinpath('templates')

class Args(NamedTuple):
    config: str
    preamble: str
    build: str
    minimal: bool
    scope: str | None
    tex_only: bool

def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        type=str,
        default='cpyc.json',
        help='The json document config file to build'
    )
    parser.add_argument(
        '-p', '--preamble',
        type=str,
        default='cpyc_preamble.tex',
        help='Use a specific preamble tex file (section in the tex prior to the \\begin{document})'
    )
    parser.add_argument(
        '-b', '--build',
        type=str,
        default='build',
        help='Path to the directory to put the build artifacts'
    )
    parser.add_argument(
        '-s', '--scope',
        type=str,
        help=(
            'If present will only render the section or entry specified '
            '(specify path from the document root to section or entry root)'
        )
    )
    parser.add_argument(
        '-t', '--tex-only',
        action='store_true',
        help='Compile the tex file only (i.e. skip compiling the pdf)'
    )
    parser.add_argument(
        '-m', '--minimal',
        action='store_true',
        help='Build the minimized version'
    )
    args = parser.parse_args()
    return Args(
        args.config,
        args.preamble,
        args.build,
        args.minimal,
        args.scope if args.scope is not None else None,
        args.tex_only
    )

def build(
    config_file: str,
    preamble_file: str,
    build: str = 'build',
    minimal: bool = False,
    scope: str | None = None,
    tex_only: bool = False,
) -> int:
    with open(config_file, 'r', encoding='utf8') as f:
        document = Document(json.load(f))
    with open(preamble_file, 'r', encoding='utf8') as f:
        preamble = f.read()
    with resources.as_file(TEMPLATES) as templates:
        generator = PDFGenerator(
            template_dir=str(templates),
            output_dir=build,
            preamble=preamble
        )
    if scope is None:
        generator.build_document(document, minimal=minimal, tex_only=tex_only)
        return 0
    section, entry, *_ = scope.split('/', maxsplit=1) + [None, None]
    if section is None:
        logging.error('Invalid scope "%s"', scope)
        return 1
    for sec in document.sections:
        if sec.path == os.path.join(document.path, section):
            if entry is None:
                generator.build_section(sec, minimal=minimal, tex_only=tex_only)
                return 0
            for ent in sec.entries:
                if ent.path == os.path.join(sec.path, entry):
                    generator.build_entry(ent, minimal=minimal, tex_only=tex_only)
                    return 0
            logging.error(
                'Invalid scope "%s" unable to locate entry "%s" in section "%s"',
                scope, entry, section
            )
            return -1
    logging.error(
        'Invalid scope "%s" unable to locate section "%s"',
        scope, section
    )
    return 1



def main() -> None:
    exit(build(*parse_args()))

if __name__ == '__main__':
    main()
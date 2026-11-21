from jinja2 import Environment, FileSystemLoader

from cpyc_buildtools.models import *

def latex_escape(value: object) -> str:
    """Escape plain text for use in LaTeX."""
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }

    return ''.join(
        replacements.get(char, char)
        for char in str(value)
    )

DEFAULT_PREAMBLE: str = r"""
\documentclass{article}
\usepackage[margin=0.5in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{parskip}
"""
class Renderer:
    def __init__(
        self,
        template_dir: str,
        preamble: str | None = None
    ) -> None:
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters['tex'] = latex_escape # pyright: ignore[reportUnknownMemberType]
        self.preamble: str = preamble if preamble is not None else DEFAULT_PREAMBLE

    def render(self, template_name: str, data: object, minimal: bool = False) -> str:
        template = self.env.get_template(template_name)
        return template.render(data=data, minimal=minimal, preamble=self.preamble)

    def render_entry(self, entry: Entry, minimal: bool = False) -> str:
        return self.render('layouts/entry.tex.j2', entry, minimal)

    def render_section(self, section: Section, minimal: bool = False) -> str:
        return self.render('layouts/section.tex.j2', section, minimal)

    def render_document(self, document: Document, minimal: bool = False) -> str:
        return self.render('layouts/document.tex.j2', document, minimal)
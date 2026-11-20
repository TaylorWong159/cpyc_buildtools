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

class Renderer:
    def __init__(self, template_dir: str) -> None:
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters['tex'] = latex_escape

    def render(self, template_name: str, data: object) -> str:
        template = self.env.get_template(template_name)
        return template.render(data=data)

    def render_entry(self, entry: Entry) -> str:
        return self.render('layouts/entry.tex.j2', entry)

    def render_section(self, section: Section) -> str:
        return self.render('layouts/section.tex.j2', section)

    def render_document(self, document: Document) -> str:
        return self.render('layouts/document.tex.j2', document)
from cpyc_buildtools.pdfgen.renderer import Renderer
from cpyc_buildtools.pdfgen.compiler import Compiler
from cpyc_buildtools.models import *

class PDFGenerator:
    def __init__(
        self,
        template_dir: str,
        output_dir: str,
    ):
        self.renderer = Renderer(template_dir)
        self.compiler = Compiler(output_dir)

    def build_entry(self, entry: Entry):
        latex = self.renderer.render_entry(entry)
        return self.compiler.compile(latex, entry.title.replace(' ', '_'))

    def build_section(self, section: Section):
        latex = self.renderer.render_section(section)
        return self.compiler.compile(latex, section.title.replace(' ', '_'))

    def build_document(self, document: Document):
        latex = self.renderer.render_document(document)
        return self.compiler.compile(latex, document.title.replace(' ', '_'))
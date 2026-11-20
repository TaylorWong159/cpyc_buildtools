import os
import subprocess

class Compiler:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def compile(self, latex: str, name: str) -> str:
        build_dir = os.path.join(self.output_dir, name)
        os.makedirs(build_dir, exist_ok=True)

        tex_file = os.path.join(build_dir, f'{name}.tex')
        with open(tex_file, 'w', encoding='utf8') as f:
            f.write(latex)

        subprocess.run(
            [
                'pdflatex',
                f'{name}.tex'
            ],
            cwd=build_dir,
            check=True,
        )

        return os.path.join(build_dir, f'{name}.pdf')
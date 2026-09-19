#!/usr/bin/env python3
"""Copy the canonical static site and adapt URLs for a GitHub Pages base path."""
import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(base_path, output):
    base_path = '/' + base_path.strip('/') if base_path.strip('/') else ''
    if base_path and not re.fullmatch(r'/[A-Za-z0-9._/-]+', base_path):
        raise ValueError('Invalid base path')
    source = ROOT / 'dist'
    output = output.resolve()
    if output == source or output in source.parents or source in output.parents:
        raise ValueError('Output must be separate from the canonical site')
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, output, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('.openai'))
    for page in output.rglob('*.html'):
        original = page.read_text()
        adapted = re.sub(r'((?:href|src)=[\"\'])/(?!/)',
                         lambda match: match[1] + base_path + '/', original)
        adapted = re.sub(r'(url=)/(?!/)',
                         lambda match: match[1] + base_path + '/', adapted)
        page.write_text(adapted)
    (output / '.nojekyll').touch()
    print(f'Prepared GitHub Pages site at {output} with base path {base_path or "/"}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-path', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.base_path, args.output)

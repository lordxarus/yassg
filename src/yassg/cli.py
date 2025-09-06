import shutil
import os
from pathlib import Path

from yassg import logger
from yassg.parser import md_to_html

import argparse

print_dbg = logger.get_print_dbg()


def crawl_md(path: Path) -> list[Path]:
    out: list[Path] = []

    out += [
        item for item in path.iterdir() if item.is_file() and item.name.endswith(".md")
    ]

    dirs: list[Path] = [it for it in path.iterdir() if it.is_dir()]

    for dir in dirs:
        out += crawl_md(dir)

    return out


def convert_to_html(files: list[Path]) -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    for file in files:
        out.append((file, md_to_html(file.read_text())))
    return out


def extract_title(file: Path) -> str:
    lns: str
    first_ln: str
    try:
        lns = file.read_text()
    except OSError as e:
        print(f"error reading {file.name}: {e.strerror}")
        return ""
    try:
        first_ln = lns.splitlines()[0]
    except IndexError:
        return ""

    return first_ln[1:] if first_ln[0] == "#" else file.name


def dir_setup(in_dir, out_dir, tmpl_path):
    if not tmpl_path.exists():
        print(f'error: template not found at "{tmpl_path}"')
        exit(-1)

    if out_dir.exists():
        shutil.rmtree(out_dir)
        os.mkdir(out_dir)
    else:
        os.mkdir(out_dir)

    static_dir_in = in_dir / "static"
    if not static_dir_in.exists():
        print(f'error: content directory "{static_dir_in}" not found')
        exit(-1)

    content_dir_in = in_dir / "content"
    if not content_dir_in.exists():
        print(f'error: content directory "{content_dir_in}" not found')
        exit(-1)

    if len(list(content_dir_in.iterdir())) == 0:
        print(f'error: no content files found in "{content_dir_in}"')
        exit(-1)


def replace_placeholders(tmpl, title, content) -> str:
    return tmpl.replace("{{ Title }}", title).replace("{{ Content }}", content)


def build(in_dir, out_dir, tmpl_path):
    dir_setup(in_dir, out_dir, tmpl_path)

    # we know that these are existent and accessible because we
    # just called dir_setup
    content_dir_in = in_dir / "content"

    shutil.copytree(in_dir / "static", out_dir, dirs_exist_ok=True)

    crawled_files = crawl_md(content_dir_in)
    converted_files = convert_to_html(crawled_files)

    rel_paths = [
        (path.relative_to(content_dir_in), html) for path, html in converted_files
    ]
    tmpl = tmpl_path.read_text()
    for rel_path, html in rel_paths:
        to_path = out_dir / rel_path
        to_path.parent.mkdir(parents=True, exist_ok=True)

        src_path = content_dir_in / rel_path
        title = extract_title(src_path)

        final_output = replace_placeholders(tmpl, title, html)

        print(f"generating {to_path.with_suffix(".html")} from {src_path}")
        to_path.with_suffix(".html").write_text(final_output)


def main():

    parser = argparse.ArgumentParser(
        prog="yassg",
        description="Create a static website from simple markdown\
                         and static files",
    )

    parser.add_argument("source_dir")
    parser.add_argument("--output_dir", default=Path("public"), required=False)
    parser.add_argument("--tmpl_path", default=Path("template.html"), required=False)

    args = parser.parse_args()

    tmpl_path = Path(args.tmpl_path)
    in_dir = Path(args.source_dir)
    out_dir = Path(args.output_dir)

    build(in_dir, out_dir, tmpl_path)


if __name__ == "__main__":
    main()

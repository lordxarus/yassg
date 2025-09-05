import shutil
import sys
import os
from pathlib import Path

from yassg import logger
from yassg.parser import md_to_html

import argparse

print_dbg = logger.get_print_dbg()


def crawl_md(path: Path) -> dict[Path, str]:
    out: dict[Path, str] = {}

    p: Path = Path(path)

    files: list[Path] = [
        item for item in p.iterdir() if item.is_file() and item.name.endswith(".md")
    ]

    for file in files:
        lines = md_to_html(file.read_text())
        # remove src dir e.g. test_site/index.md -> index.md
        out[file] = lines

    dirs: list[Path] = [it for it in p.iterdir() if it.is_dir()]
    for dir in dirs:
        out.update(crawl_md(dir))
    return out


def extract_title(ln: str) -> str:
    if ln[0] != "#":
        raise ValueError(f"looking for # got {ln[0]}")
    return ln[1:]


def build(in_dir, out_dir, tmpl_path):
    if not tmpl_path.exists():
        print(f'error: template not found at "{tmpl_path}"')
        exit(-1)

    if out_dir.exists():
        shutil.rmtree(out_dir)
        os.mkdir(out_dir)
    else:
        os.mkdir(out_dir)

    static_dir_in = in_dir / "static"
    if static_dir_in.exists():
        shutil.copytree(static_dir_in, out_dir, dirs_exist_ok=True)

    content_dir_in = in_dir.joinpath(Path("content"))
    if not content_dir_in.exists():
        print(f'error: content directory "{content_dir_in}" not found')
        exit(-1)
    if len(list(content_dir_in.iterdir())) == 0:
        print(f'error: no content files found in "{content_dir_in}"')
        exit(-1)

    crawled_paths = crawl_md(content_dir_in).items()
    rel_paths = [
        (path.relative_to(content_dir_in), html) for path, html in crawled_paths
    ]

    for rel_path, html in rel_paths:
        to_path = out_dir / rel_path
        to_path.parent.mkdir(parents=True, exist_ok=True)

        src_path = content_dir_in / rel_path
        md_content = src_path.read_text()
        title = extract_title(md_content.splitlines()[0])
        title = title[1:] if title[0] == " " else title

        output = (
            tmpl_path.read_text()
            .replace("{{ Title }}", title)
            .replace("{{ Content }}", html)
        )
        print(f"generating {to_path.with_suffix(".html")} from {src_path}")
        to_path.with_suffix(".html").write_text(output)


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

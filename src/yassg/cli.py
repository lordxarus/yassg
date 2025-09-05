import shutil
import sys
import os
from pathlib import Path

from yassg import logger
from yassg.parser import md_to_html

default_mappings = {"static": "", "content": ""}

print_dbg = logger.get_print_dbg()


def extract_title(ln: str) -> str:
    if ln[0] != "#":
        raise ValueError(f"looking for # got {ln[0]}")
    return ln[1:]



def main():
    if len(sys.argv) < 2:
        print("usage: yassg <source dir or file> [output dir]")
        exit(22)
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("usage: yassg <source dir or file> [output dir]\n")
        print("source dir must have directories static and content\n")
        exit(0)

    tmpl_path = Path("template.html")

    if not tmpl_path.exists():
        print(f"error: template not found at {tmpl_path}/")
        exit(-1)
    tmpl = tmpl_path.read_text()

    in_dir = Path(sys.argv[1])
    default_mappings[in_dir.as_posix()] = ""
    out_dir: Path = Path("public")

    if len(sys.argv) > 2:
        out_dir = Path(sys.argv[2])
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
        print(f"error: content directory {content_dir_in}/ not found")
        exit(-1)
    if len(list(content_dir_in.iterdir())) == 0:
        print(f"error: no content files found in {content_dir_in}/")
        exit(-1)

    def crawl_md(path: Path) -> dict[Path, str]:
        out: dict[Path, str] = {}

        p: Path = Path(path)

        files: list[Path] = [
            item for item in p.iterdir() if item.is_file() and item.name.endswith(".md")
        ]

        for file in files:
            lines = md_to_html(file.read_text())
            # remove src dir e.g. test_site/index.md -> index.md
            out[file.relative_to(content_dir_in)] = lines

        dirs: list[Path] = [it for it in p.iterdir() if it.is_dir()]
        for dir in dirs:
            out.update(crawl_md(dir))
        return out

    for rel_file_path, html in crawl_md(content_dir_in).items():
        to_path = out_dir / rel_file_path
        to_path.parent.mkdir(parents=True, exist_ok=True)

        src_path = (content_dir_in / rel_file_path)
        md_content = src_path.read_text()
        title = extract_title(md_content.splitlines()[0])
        title = title[1:] if title[0] == " " else title

        output = tmpl_path.read_text().replace("{{ Title }}", title).replace("{{ Content }}", html)
        print(f"generating {to_path.with_suffix(".html")} from {src_path}")
        to_path.with_suffix(".html").write_text(output)


if __name__ == "__main__":
    main()

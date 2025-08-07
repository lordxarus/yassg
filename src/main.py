import shutil
from copy import deepcopy
import subprocess
import sys
import os
from pathlib import Path

import logger
from parser import md_to_html

default_mappings = {"static": "", "content": ""}

print_dbg = logger.get_print_dbg()


def extract_title(ln: str) -> str:
    if ln[0] != "#":
        raise ValueError(f"looking for # got {ln[0]}")
    return ln[1:]


def apply_mappings(p: Path, mappings: dict[str, str]) -> Path:
    new_parts = []
    for part in p.parts:
        if mappings is None or part not in mappings:
            new_parts.append(part)
        elif part in mappings:
            mapped = mappings[part]
            if mapped != "":
                new_parts.append(mappings[part])
    return Path("/".join(new_parts))


def copy_recursive(file: Path, to_path: Path, mappings: dict[str, str] = None):

    if file.is_dir():
        for f in file.iterdir():
            copy_recursive(f, to_path, mappings)
            # f = Path([prt for prt in f.parts if ])

            # remove in_dir from path
    else:
        # get source dir root
        in_dir = Path("/".join(file.parts[:1]))
        f = Path("/".join(file.parts[1:]))
        mapped = apply_mappings(f, default_mappings)
        mkdir_with_parents(get_parent_dir(to_path.joinpath(mapped)))
        shutil.copy(file, to_path.joinpath(mapped))


def mkdir_with_parents(path: Path):
    rest = path.parts
    cand = Path()

    while len(rest) > 0:
        cand = cand.joinpath(Path(rest[0]))
        rest = rest[1:]

        if not cand.exists():
            cand.mkdir()
            print_dbg(f"creating directory {cand}")


def get_parent_dir(file: Path) -> Path:
    parts = file.parts
    if len(parts) == 2:
        print_dbg(f"special case len(file.parts) == 2 for {file}")
    return Path("/".join(file.parts[:-1]))


def generate_page(from_path: Path, tmpl: str, to_path: Path, txt: str):
    if not from_path.exists():
        raise FileNotFoundError("from_path does not exist")

    print(
        f"generating {to_path.joinpath(apply_mappings(from_path, default_mappings))} from {from_path}..."
    )

    mkdir_with_parents(Path(to_path.as_posix().replace(to_path.name, "")))
    content = from_path.read_text()
    title = extract_title(content.splitlines()[0])
    title = title[1:] if title[0] == " " else title

    return tmpl.replace("{{ Title }}", title).replace("{{ Content }}", txt)


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

    static_dir_in = in_dir.joinpath(Path("static"))
    if static_dir_in.exists():
        for file in list(static_dir_in.iterdir()):
            # remove <in_dir>/static/
            # TODO: Test this!
            out_file = apply_mappings(file, default_mappings)
            # out_file = Path(
            #     "/".join(
            #         [f for f in file.parts if f != "static" and f != in_dir.parts[0]]
            #     )
            # )
            copy_recursive(file, out_dir, {"static": ""})

    content_dir_in = in_dir.joinpath(Path("content"))
    if not content_dir_in.exists():
        print(f"error: content directory {content_dir_in}/ not found")
        exit(-1)
    if len(list(content_dir_in.iterdir())) == 0:
        print(f"error: no content files found in {content_dir_in}/")
        exit(-1)

    def crawl_md(path: Path) -> dict[str, str]:
        out: dict[str, str] = {}

        p: Path = Path(path)

        files: list[Path] = [
            item for item in p.iterdir() if item.is_file() and item.name.endswith(".md")
        ]

        for file in files:
            lines = md_to_html(file.read_text())
            # remove src dir e.g. test_site/index.md -> index.md
            pth = Path("/".join(file.parts[1:]))
            out[pth.as_posix()] = lines

        dirs: list[Path] = [it for it in p.iterdir() if it.is_dir()]
        for dir in dirs:
            out.update(crawl_md(dir))
        return out

    for name, html in crawl_md(content_dir_in).items():
        name_path: Path = Path(name.rstrip(".md") + ".html")
        # TODO test this!
        name_path = apply_mappings(name_path, default_mappings)
        # name_path = Path(
        #     "/".join([part for part in name_path.parts if part != "content"])
        # )
        out_path = out_dir.joinpath(name_path)

        out_path_parent_dir = get_parent_dir(out_path)
        mkdir_with_parents(out_path_parent_dir)
        out_path.write_text(
            generate_page(in_dir.joinpath(Path(name)), tmpl, out_dir, html)
        )


if __name__ == "__main__":
    main()

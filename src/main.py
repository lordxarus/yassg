import shutil
from copy import deepcopy
import subprocess
import sys
import os
from pathlib import Path

from parser import md_to_html


def extract_title(ln: str) -> str:
    if ln[0] != "#":
        raise ValueError(f"looking for # got {ln[0]}")
    return ln[1:]


def copy_recursive(file: Path, to_path: Path, mappings: dict[str, str] = None):
    print(to_path)

    def apply_mappings(p: Path) -> Path:
        new_parts = []
        for part in p.parts:
            if mappings is None or part not in mappings:
                new_parts.append(part)
            elif part in mappings:
                mapped = mappings[part]
                if mapped != "":
                    new_parts.append(mappings[part])
        return Path("/".join(new_parts))

    if file.is_dir():
        for f in file.iterdir():
            copy_recursive(f, to_path, mappings)
            # f = Path([prt for prt in f.parts if ])

            # remove in_dir from path
    else:
        in_dir = Path("/".join(file.parts[:1]))
        f = Path("/".join(file.parts[1:]))
        mapped = apply_mappings(f)
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
            print(f"creating directory {cand}")


def get_parent_dir(file: Path) -> Path:
    parts = file.parts
    if len(parts) == 2:
        print(f"special case: {file}")
    return Path("/".join(file.parts[:-1]))


def generate_page(from_path: Path, tmpl: str, to_path: Path, txt: str):
    if not from_path.exists():
        raise FileNotFoundError("from_path does not exist")

    print(f"generating {to_path} from {from_path}...")

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
    out_dir: Path = Path("public")

    if len(sys.argv) > 2:
        out_dir = Path(sys.argv[2])
    if out_dir.exists():
        shutil.rmtree(out_dir)
        os.mkdir(out_dir)
    else:
        os.mkdir(out_dir)

    # static_dir_out = out_dir.joinpath(Path("static"))
    # if not static_dir_out.exists():
    #     mkdir_with_parents(static_dir_out)

    static_dir_in = in_dir.joinpath(Path("static"))
    if static_dir_in.exists():
        # print([Path("/".join(file.parts)) for file in list(static_dir_in.iterdir())])
        for file in list(static_dir_in.iterdir()):
            # remove <in_dir>/static/
            out_file = Path(
                "/".join(
                    [f for f in file.parts if f != "static" and f != in_dir.parts[0]]
                )
            )
            print(f"file == {out_file}")
            copy_recursive(file, out_dir, {"static": ""})
        # for p in static_dir_in.iterdir():
        #     print(p)
        #     if p.is_file():
        #         print(f"copying file {out_dir}")
        #         shutil.copy(p, out_dir)
        #     else:

        #         print(f"else: {out_dir.joinpath(Path("/".join(p.parts[2:])))}")
        #         copy_recursive(
        #             list(static_dir_in.iterdir()),
        #             out_dir.joinpath(Path("/".join(p.parts[2:]))),
        #         )

    # content_dir_out = out_dir.joinpath(Path("content"))
    # if not content_dir_out.exists():
    #     mkdir_with_parents(content_dir_out)
    content_dir_in = in_dir.joinpath(Path("content"))
    if not content_dir_in.exists():
        print(f"error: content directory {content_dir_in}/ not found")
        exit(-1)
    if len(list(content_dir_in.iterdir())) == 0:
        print(f"error: no content files found in {content_dir_in}/")
        exit(-1)

    def crawl(path: Path) -> dict[str, str]:
        out: dict[str, str] = {}

        p: Path = Path(path)

        files: list[Path] = [
            item for item in p.iterdir() if item.is_file() and item.name.endswith(".md")
        ]

        for file in files:
            lines = md_to_html(file.read_text())
            pth = Path("/".join(file.parts[1:]))
            out[pth.as_posix()] = lines

        dirs: list[Path] = [it for it in p.iterdir() if it.is_dir()]
        for dir in dirs:
            out.update(crawl(dir))
        return out

    for name, html in crawl(content_dir_in).items():
        name_path: Path = Path(name.rstrip(".md") + ".html")
        name_path = Path(
            "/".join(
                [
                    part
                    for part in name_path.parts
                    if part != "content" and part != "static"
                ]
            )
        )
        out_path = out_dir.joinpath(name_path)

        out_path_parent_dir = get_parent_dir(out_path)
        mkdir_with_parents(out_path_parent_dir)
        out_path.write_text(
            generate_page(in_dir.joinpath(Path(name)), tmpl, out_dir, html)
        )


main()

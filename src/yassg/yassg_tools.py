import shutil
from pathlib import Path
import logging

from yassg.parser import md_to_html

logger = logging.getLogger(__name__)


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


def extract_title(file: Path) -> str | None:
    """Extracts an h1 heading on the first line.

    Returns:
        The title string if found, otherwise None
    """
    lns: str
    first_ln: str
    lns = file.read_text()
    # review: i believe this to be correct because we don't want to fail loudly
    # or silently here
    try:
        first_ln = lns.splitlines()[0]
    except IndexError:
        logger.warning(f"found {file.name} to be empty in extract_title")
        return None

    return first_ln[1:] if first_ln and first_ln[0] == "#" else None


def dir_setup(in_dir: Path, out_dir: Path, tmpl: Path):
    if not tmpl.exists(follow_symlinks=False):
        raise FileNotFoundError(f'error: template not found at "{tmpl}"')

    if out_dir.exists(follow_symlinks=False):
        shutil.rmtree(out_dir)

    out_dir.mkdir()

    static_dir_in = in_dir / "static"
    if not static_dir_in.exists(follow_symlinks=False):
        raise NotADirectoryError(
            f'error: content directory "{static_dir_in}" not found'
        )

    content_dir_in = in_dir / "content"
    if not content_dir_in.exists(follow_symlinks=False):
        raise FileNotFoundError(
            f'error: content directory "{content_dir_in}" not found'
        )

    if len(list(content_dir_in.iterdir())) == 0:
        raise FileNotFoundError(f'error: no content files found in "{content_dir_in}"')


def replace_placeholders(tmpl, title, content) -> str:
    return tmpl.replace("{{ Title }}", title).replace("{{ Content }}", content)


def build(in_dir: Path, out_dir: Path, tmpl_path: Path) -> None:
    """Orchestrates the various parts of yassg to generate a site at out_dir

    Returns:
        None
    Raises:
        PermissionError, OSError
    """
    dir_setup(in_dir, out_dir, tmpl_path)

    # we know that these are existent and accessible because we
    # just called dir_setup
    content_dir_in = in_dir / "content"

    shutil.copytree(in_dir / "static", out_dir, dirs_exist_ok=True)

    crawled_files = crawl_md(content_dir_in)
    converted_files: list[tuple[Path, str]]
    converted_files = convert_to_html(crawled_files)

    rel_paths = [
        (path.relative_to(content_dir_in), html) for path, html in converted_files
    ]

    tmpl = tmpl_path.read_text()
    for rel_path, html in rel_paths:
        to_path = out_dir / rel_path
        to_path.parent.mkdir(parents=True, exist_ok=True)

        src_path = content_dir_in / rel_path
        title: str
        title = extract_title(src_path) or src_path.name

        final_output = replace_placeholders(tmpl, title, html)

        logger.info(f"generating {to_path.with_suffix(".html")} from {src_path}")
        to_path.with_suffix(".html").write_text(final_output)

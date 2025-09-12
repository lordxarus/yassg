from dataclasses import dataclass
import subprocess
from typing import Generator, Self
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup

TEMPLATE_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" type="text/css" rel="stylesheet" />
  </head>

  <body>
    <article>{{ Content }}</article>
  </body>
</html>"""

INDEX_MD = """
# The Index

Welcome to my website :)
"""

INDEX_CSS = """
body {
    color: red;
}
"""


@dataclass
class SitePath:
    src_dir: Path
    out_dir: Path

    @property
    def static_dir(self: Self) -> Path:
        return self.src_dir / "static"

    @property
    def content_dir(self: Self) -> Path:
        return self.src_dir / "content"

    @property
    def template_path(self: Self) -> Path:
        return self.src_dir / "static"


@pytest.fixture
def site_setup() -> Generator[SitePath]:
    with TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)

        src_dir = base_dir / "sample_site"
        src_dir.mkdir(parents=True)

        template_path = src_dir / "template.html"

        static_dir = src_dir / "static"
        static_dir.mkdir(parents=True)

        content_dir = src_dir / "content"
        content_dir.mkdir(parents=True)

        out_dir = base_dir / "public"
        out_dir.mkdir(parents=True)

        (src_dir / "template.html").write_text(TEMPLATE_HTML)
        (content_dir / "index.md").write_text(INDEX_MD)
        (static_dir / "index.css").write_text(INDEX_CSS)

        yield SitePath(
            src_dir=src_dir,
            out_dir=out_dir,
        )


def test_happy_build(site_setup):
    """ """
    site_path: SitePath = next(site_setup)

from pathlib import Path

from yassg.yassg_tools import build

import argparse
import logging

import sys
import importlib.resources

logger = logging.getLogger(__name__)


def main():

    with importlib.resources.as_file(
        (importlib.resources.files("yassg") / "template.html")
    ) as default_tmpl_path:
        log_level = logging.DEBUG
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s: %(message)s",
        )

        parser = argparse.ArgumentParser(
            prog="yassg",
            description="Create a static website from simple markdown\
                             and static files",
        )

        parser.add_argument("source_dir")
        parser.add_argument("--output_dir", default=Path("public"), required=False)
        parser.add_argument("--template", default=default_tmpl_path, required=False)

        args = parser.parse_args()

        tmpl_path = Path(args.tmpl_path)
        in_dir = Path(args.source_dir)
        out_dir = Path(args.output_dir)

        try:
            build(in_dir, out_dir, tmpl_path)
        except (OSError, FileNotFoundError, PermissionError) as e:
            logger.critical(f"failed to build {e}")
            sys.exit(-1)


if __name__ == "__main__":
    main()

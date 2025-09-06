from pathlib import Path

from yassg.yassg_tools import build

import argparse
import logging

logger = logging.getLogger(__name__)


def main():

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
    parser.add_argument("--tmpl_path", default=Path("template.html"), required=False)

    args = parser.parse_args()

    tmpl_path = Path(args.tmpl_path)
    in_dir = Path(args.source_dir)
    out_dir = Path(args.output_dir)

    try:
        build(in_dir, out_dir, tmpl_path)
    except (OSError, FileNotFoundError, PermissionError) as e:
        logger.critical(f"failed to build {e}")


if __name__ == "__main__":
    main()

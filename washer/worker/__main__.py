import argparse
import os

from .worker import prepare_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--unset",
        nargs="*",
        help="Unregister environment var")

    args = parser.parse_args()

    # Unregister env vars to properly run subcommands when compiled with
    # nuitka.
    if args.unset:
        for name in args.unset:
            os.environ.pop(name)

    # Prepare & run the app.
    app = prepare_app()
    app.run()


if __name__ == '__main__':
    main()

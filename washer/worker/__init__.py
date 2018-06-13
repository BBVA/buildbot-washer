import argparse
import os

from .worker import prepare_app


def load_tasks(filename):
    from importlib.machinery import SourceFileLoader
    return SourceFileLoader('washer.tasks', filename).load_module()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--unset",
        nargs="*",
        help="Unregister environment var")
    parser.add_argument(
        "tasks_file",
        help="Python file implementing washer tasks.")

    args = parser.parse_args()

    # Unregister env vars to properly run subcommands when compiled with
    # nuitka.
    if args.unset:
        for name in args.unset:
            os.environ.pop(name)

    # Load Washer tasks from user file.
    load_tasks(args.tasks_file)

    # Prepare & run the app.
    app = prepare_app()
    app.run()

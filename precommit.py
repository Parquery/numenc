#!/usr/bin/env python3
"""
Runs precommit checks on the repository.
"""
import argparse
import concurrent.futures
import os
import pathlib
import subprocess
import sys
from typing import List, Union, Tuple  # pylint: disable=unused-import

import yapf.yapflib.yapf_api


def check(path: pathlib.Path, py_dir: pathlib.Path,
          overwrite: bool) -> Union[None, str]:
    """
    Runs all the checks on the given file.

    :param path: to the source file
    :param py_dir: path to the source files
    :param overwrite: if True, overwrites the source file in place instead of
        reporting that it was not well-formatted.
    :return: None if all checks passed. Otherwise, an error message.
    """
    style_config = py_dir / 'style.yapf'

    report = []

    # yapf
    if not overwrite:
        formatted, _, changed = yapf.yapflib.yapf_api.FormatFile(
            filename=str(path), style_config=str(style_config), print_diff=True)

        if changed:
            report.append("Failed to yapf {}:\n{}".format(path, formatted))
    else:
        yapf.yapflib.yapf_api.FormatFile(
            filename=str(path), style_config=str(style_config), in_place=True)

    # mypy
    env = os.environ.copy()
    env['PYTHONPATH'] = ":".join([py_dir.as_posix(), env.get("PYTHONPATH", "")])

    proc = subprocess.Popen(
        ['mypy', str(path), '--ignore-missing-imports'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        universal_newlines=True)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        report.append("Failed to mypy {}:\nOutput:\n{}\n\n"
                      "Error:\n{}".format(path, stdout, stderr))

    # pylint
    proc = subprocess.Popen(
        ['pylint',
         str(path), '--rcfile={}'.format(py_dir / 'pylint.rc')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        report.append("Failed to pylint {}:\nOutput:\n{}\n\n"
                      "Error:\n{}".format(path, stdout, stderr))

    if len(report) > 0:
        return "\n".join(report)

    return None


def build_and_install_module(root_dir: pathlib.Path) -> bool:
    """
    Builds and installs the C++ code for Pynumenc.

    :param root_dir: the project's root directory
    :return: True if the C++ code was built and installed correctly,
    False otherwise.
    """
    setup_path = root_dir / 'setup.py'

    build_proc = subprocess.Popen(
        ['python3', str(setup_path), 'build'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    stdout, stderr = build_proc.communicate()
    if build_proc.returncode != 0:
        print("Failed to build the C++ module through {}:\nOutput:\n{}"
              "\n\nError:\n{}".format(setup_path, stdout, stderr))
        return False

    install_proc = subprocess.Popen(
        ['python3', str(setup_path), 'install'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    stdout, stderr = install_proc.communicate()
    if install_proc.returncode != 0:
        print("Failed to install the C++ module through {}:\nOutput:\n{}"
              "\n\nError:\n{}".format(setup_path, stdout, stderr))
        return False

    return True


def main() -> int:
    """"
    Main routine
    """
    # pylint: disable=too-many-locals
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        help=
        "Overwrites the unformatted source files with the well-formatted code "
        "in place. If not set, an exception is raised if any of the files do "
        "not conform to the style guide.",
        action='store_true')

    args = parser.parse_args()

    overwrite = bool(args.overwrite)

    py_dir = pathlib.Path(__file__).parent

    # yapf: disable
    pths = sorted(
        list(py_dir.glob("*.py")) +
        list((py_dir / 'tests').glob("*.py")))
    # yapf: enable

    print("Building the C++ module...")
    success = build_and_install_module(py_dir)
    if not success:
        return 1
    else:
        print("Succesfully built the C++ module.")

    print("There are {} file(s) that need to be individually "
          "checked...".format(len(pths)))

    futures_paths = [
    ]  # type: List[Tuple[concurrent.futures.Future, pathlib.Path]]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for pth in pths:
            future = executor.submit(
                fn=check, path=pth, py_dir=py_dir, overwrite=overwrite)
            futures_paths.append((future, pth))

        for future, pth in futures_paths:
            report = future.result()
            if report is None:
                print("Passed all checks: {}".format(pth))
            else:
                print(
                    "One or more checks failed for {}:\n{}".format(pth, report))
                success = False

    print("Doctesting...")
    subprocess.check_call(
        ["python3", "-m", "doctest", (py_dir / "README.rst").as_posix()])

    print("Running unit tests...")
    source_dir = pathlib.Path(__file__).resolve().parent
    retcode = subprocess.call(
        ['python3', '-m', 'unittest', 'discover',
         str(source_dir / 'tests')])
    success = success and retcode == 0

    if not success:
        print("One or more checks failed.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

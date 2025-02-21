import os
import shutil
import argparse
import subprocess
import unittest

import sys
from datetime import datetime
import ftplib
import glob
from pathlib import Path
from rickle import __version__ as version_name

_project_name = 'rickle'
_git_files_for_add = [
    "./docs/source/*.rst",
    f"./{_project_name}/__init__.py",
    f"./{_project_name}/__version__.py"
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def upload_to_pypi(release_name):
    from twine.commands import upload

    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.WARNING}-- Using version {version_name}!{bcolors.ENDC}')

    if release_name and release_name.lower() in ['master', 'test', 'development']:
        raise ValueError('May not rename wheel to {}. To deploy a wheel by that name, checkout that branch')

    if not release_name:
        release_name = version_name

    release_name = release_name.replace("-", "_")
    local_file = f"dist/{_project_name}-{version_name}.tar.gz"
    remote_file = f"{_project_name}-{release_name}.tar.gz"

    os.mkdir('deploy')
    shutil.copy(local_file, f"deploy/{remote_file}")

    print(f"{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.OKBLUE}-- Deploying [{local_file}] -> [{remote_file}]{bcolors.ENDC}")

    upload.main(['deploy/*', '-u', os.getenv('TWINE_USERNAME'), '-p', os.getenv('TWINE_PASSWORD')])

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}-- Deployed!{bcolors.ENDC}")

def build_documentation():
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Change dir and make HTML docs{bcolors.ENDC}')
    os.chdir('./docs')
    if sys.platform == "win32":
        os.system('make.bat html')
    else:
        os.system('make html')
    os.chdir('..')
    print(f'{bcolors.UNDERLINE}-- Made docs, change dir{bcolors.ENDC}')

def lock_and_gen_pipreq(provider='poetry'):
    if provider.lower().strip() == 'pipenv':
        print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Locking Pipfile.lock and generating requirements.txt{bcolors.ENDC}')

        os.system("pipenv lock -r > requirements.txt")
    if provider.lower().strip() == 'poetry':
        print(
            f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Locking poetry.lock and generating requirements.txt{bcolors.ENDC}')

        os.system("poetry export -f requirements.txt --output requirements.txt")

def upload_docs_via_ftp():
    from dotenv import load_dotenv
    load_dotenv()
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Upload documentation to FTP server! {bcolors.ENDC}')
    try:
        with ftplib.FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USERNAME'), os.getenv('FTP_PASSWORD')) as ftp:
            ftp.cwd(os.getenv('FTP_DIRECTORY'))
            ftp.set_pasv(True)

            for f in glob.glob('./docs/build/html/*'):
                if os.path.isfile(f):
                    with open(f, 'rb') as _f:
                        file_path = Path(f)
                        try:
                            ftp.storlines(f'STOR {file_path.name}', _f)
                            print(f"{bcolors.OKBLUE}Uploaded: {file_path.name}{bcolors.ENDC}")
                        except Exception as exc:
                            print(f"{bcolors.FAIL}{bcolors.BOLD}-- ERROR: {f} {str(exc)}!{bcolors.ENDC}")

            ftp.cwd('../../..')
            ftp.cwd(os.getenv('FTP_DIRECTORY') + '/coverage')

            for f in glob.glob('./coverage_report/unittests/*'):
                if os.path.isfile(f):
                    with open(f, 'rb') as _f:
                        file_path = Path(f)
                        try:
                            ftp.storlines(f'STOR {file_path.name}', _f)
                            print(f"{bcolors.OKBLUE}Uploaded: {file_path.name}{bcolors.ENDC}")
                        except Exception as exc:
                            print(f"{bcolors.FAIL}{bcolors.BOLD}-- ERROR: {f} {str(exc)}!{bcolors.ENDC}")
    except Exception as exc:
        print(f"{bcolors.FAIL}{bcolors.BOLD}-- ERROR: {f} {str(exc)}!{bcolors.ENDC}")
        return

    print(f'{bcolors.UNDERLINE}-- Docs uploaded! {bcolors.ENDC}')

def build_wheel():
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Deleting artefacts and building wheel{bcolors.ENDC}')
    delete_build()
    delete_dist()
    os.system("python setup.py sdist bdist_wheel")

def delete_build():
    if sys.platform == "win32":
        os.system("RMDIR build /s /q")
        os.system(f"RMDIR {_project_name}.egg-info /s /q")

    else:
        os.system("rm -rf build")
        os.system(f"rm -rf {_project_name}.egg-info" )


def delete_dist():
    if sys.platform == "win32":
        os.system("RMDIR -f dist /s /q")
        os.system("RMDIR deploy /s /q")
    else:
        os.system("rm -rf dist")
        os.system("rm -rf deploy" )

def specified_tests(tests):
    for test in tests:
        file_name = '%s.py' % test
        tests = unittest.TestLoader().discover(start_dir="./tests/unittest", pattern=file_name, top_level_dir=".")
        unittest.TextTestRunner(verbosity=4).run(tests)
        tests = unittest.TestLoader().discover(start_dir="./tests/integration", pattern=file_name, top_level_dir=".")
        unittest.TextTestRunner(verbosity=4).run(tests)

def all_unit_tests(do_coverage=False):
    import coverage
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Running all unit tests!{bcolors.ENDC}')
    cov = coverage.Coverage(cover_pylib=False, data_file='.unittest')
    if do_coverage:
        cov.start()

    tests = unittest.TestLoader().discover(start_dir="./tests/unittest", pattern="test_*.py", top_level_dir=".")
    result = unittest.TextTestRunner(verbosity=4).run(tests)
    if do_coverage:
        cov.stop()
        cov.save()
        cov.html_report(directory='coverage_report/unittests')
    return result.wasSuccessful()

def all_integration_tests(do_coverage=False):
    import coverage
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Running all integration tests!{bcolors.ENDC}')
    cov = coverage.Coverage(cover_pylib=False, data_file='.integration')
    if do_coverage:
        cov.start()

    tests = unittest.TestLoader().discover(start_dir="./tests/integration", pattern="test_*.py", top_level_dir=".")
    result = unittest.TextTestRunner(verbosity=4).run(tests)
    if do_coverage:
        cov.stop()
        cov.save()
        cov.html_report(directory='coverage_report/integration')
    return result.wasSuccessful()

def bump_version_patch(with_poetry=True):
    if with_poetry:
        result = subprocess.Popen("poetry version patch -s",
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
        version_name = result.stdout.read().strip()

        with open(f"{_project_name}/__version__.py", "r") as f:
            lines = f.readlines()
            lines[0] = f"__version__ = '{version_name}'\n"
            lines[1] = f'__date__ = "{datetime.today().strftime("%Y-%m-%d")}"\n'
        if lines:
            with open(f"{_project_name}/__version__.py", "w") as f:
                f.writelines(lines)
    else:

        with open(f"{_project_name}/__version__.py", "r") as f:
            lines = f.readlines()
            v = version_name.split('.')
            major = int(v[0])
            minor = int(v[1])
            patch = int(v[2]) + 1
            lines[0] = f"__version__ = '{major}.{minor}.{patch}'\n"
            lines[1] = f'__date__ = "{datetime.today().strftime("%Y-%m-%d")}"\n'
        if lines:
            with open(f"{_project_name}/__version__.py", "w") as f:
                f.writelines(lines)

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}-- Version number bumped to {version_name}!{bcolors.ENDC}")

def add_files_for_commit():
    for f in _git_files_for_add:
        os.system(f"git add {f}")

def main(args):
    if not all_unit_tests(args.coverage):
        print(f'{bcolors.FAIL}{bcolors.BOLD}Unit testing failed, not building!{bcolors.ENDC}')
        return

    if not all_integration_tests(args.coverage):
        print(f'{bcolors.FAIL}{bcolors.BOLD}Integration testing failed, not building!{bcolors.ENDC}')
        return

    if args.pipreq:
        lock_and_gen_pipreq()

    if args.build or args.deploy:
        bump_version_patch()

        build_wheel()

    if args.deploy:
        upload_to_pypi(args.remotename)

    if args.sphinx:
        build_documentation()

    if args.ftp:
        upload_docs_via_ftp()

    if args.remove:
        delete_build()
        delete_dist()

    if args.git:
        add_files_for_commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"""
        Builds {_project_name} libs package, runs tests, builds docs, and deploys to PyPi.
        """,
    )
    parser.add_argument(
        "--build",
        "-b",
        help="Build wheel, not required if -d is used",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--remove",
        "-r",
        help="Removes build artifacts",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--unit",
        "-u",
        help="Pre-run all unit tests",
        action="store_true",
    )
    parser.add_argument(
        "--integration",
        "-i",
        help="Pre-run all integration tests",
        action="store_true",
    )
    parser.add_argument(
        "--coverage",
        "-c",
        help="Run coverage over tests",
        action="store_true",
    )
    parser.add_argument(
        '-t',
        '--tests',
        nargs='+',
        help='Define a list of python test files to run, Usage: -t test_data test_utils'
    )
    parser.add_argument(
        "--deploy",
        "-d",
        help="Deploys the built package to PyPi",
        action="store_true",
    )
    parser.add_argument(
        "--remotename",
        type=str,
        default=None,
        help="Define release name for remote object")
    parser.add_argument(
        "--pipreq",
        "-p",
        help="Lock pipenv dependencies and generate requirements.txt",
        action="store_true",
    )
    parser.add_argument(
        "--sphinx",
        "-s",
        help="Builds the sphinx documentation",
        action="store_true",
    )
    parser.add_argument(
        "--ftp",
        "-f",
        help="Uploads the generated documentation via FTP",
        action="store_true",
    )

    parser.add_argument(
        "--git",
        "-g",
        help="Add usual files for commit",
        action="store_true",
    )

    main(parser.parse_args())
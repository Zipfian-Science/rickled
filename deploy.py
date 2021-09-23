import os
import shutil
import argparse
import run_tests as tests
import sys
from twine.commands import upload
import json
import ftplib
import glob
from pathlib import Path

_project_name = 'pickle_rick'

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
    with open("version.json", "r") as f:
        version = json.load(f)

    version_name = '{major}.{minor}.{patch}'.format(**version)

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

def lock_and_gen_pipreq():
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Locking Pipfile.lock and generating requirements.txt{bcolors.ENDC}')
    os.system("pipenv lock -r > requirements.txt")

def upload_docs_via_ftp():
    print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Upload documentation to FTP server! {bcolors.ENDC}')
    try:
        with ftplib.FTP(os.getenv('FTP_HOST'), os.getenv('FTP_USERNAME'), os.getenv('FTP_PASSWORD')) as ftp:
            ftp.cwd(os.getenv('FTP_DIRECTORY'))

            for f in glob.glob('./docs/build/html/*'):
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

def do_unit_tests(args):
    if args.unit:
        print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Running all unit tests!{bcolors.ENDC}')
        return tests.all_unit_tests(args.coverage)
    return True


def do_integration_tests(args):
    if args.integration:
        print(f'{bcolors.UNDERLINE}{bcolors.BOLD}{bcolors.HEADER}-- Running all integration tests!{bcolors.ENDC}')
        return tests.all_integration_tests(args.coverage)
    return True


def main(args):
    if not do_unit_tests(args):
        print(f'{bcolors.FAIL}{bcolors.BOLD}Unit testing failed, not building!{bcolors.ENDC}')
        return

    if not do_integration_tests(args):
        print(f'{bcolors.FAIL}{bcolors.BOLD}Integration testing failed, not building!{bcolors.ENDC}')
        return

    if args.pipreq:
        lock_and_gen_pipreq()

    if args.build or args.deploy:
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

    if args.deploy:
        # All went well!
        with open("version.json", "r") as f:
            version = json.load(f)

        version['patch'] += 1
        with open("version.json", "w") as f:
            json.dump(version, f)

        with open(f"{_project_name}/__init__.py", "r") as f:
            lines = f.readlines()
            lines[0] = "__version__ = '{major}.{minor}.{patch}'\n".format(**version)
        if lines:
            with open(f"{_project_name}/__init__.py", "w") as f:
                f.writelines(lines)

        print(f"{bcolors.OKGREEN}{bcolors.BOLD}-- Version number bumped to {version}!{bcolors.ENDC}")


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
        default=True
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

    main(parser.parse_args())

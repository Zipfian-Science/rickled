import argparse
import unittest
import coverage

def specified_tests(tests):
    for test in tests:
        file_name = '%s.py' % test
        tests = unittest.TestLoader().discover(start_dir="./tests/unittest", pattern=file_name, top_level_dir=".")
        unittest.TextTestRunner(verbosity=4).run(tests)
        tests = unittest.TestLoader().discover(start_dir="./tests/integration", pattern=file_name, top_level_dir=".")
        unittest.TextTestRunner(verbosity=4).run(tests)

def all_unit_tests(do_coverage=False):
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

def main(args):
    if args.tests:
        specified_tests(args.tests)
    if args.unit:
        all_unit_tests(args.coverage)
    if args.integration:
        all_integration_tests(args.coverage)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Runs tests for Pickle Rick including unit, integration, and coverage tests.
        """,
    )
    parser.add_argument(
        "--unit",
        "-u",
        help="Run all unit tests",
        action="store_true",
    )
    parser.add_argument(
        "--integration",
        "-i",
        help="Run all integration tests",
        action="store_true",
    )
    parser.add_argument(
        "--coverage",
        "-c",
        help="Run coverage over selected tests",
        action="store_true",
        default=False
    )
    parser.add_argument(
        '-t',
        '--tests',
        nargs='+',
        help='Define a list of python test files to run, Usage: python run_tests.py -t test_data test_utils'
    )

    main(parser.parse_args())

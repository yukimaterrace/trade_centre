import argparse

from classes.test import api_test, algorithm_test
from classes.trade import trade
from classes.progress_viewer import progress_view


def get_args():
    parser = argparse.ArgumentParser('python src/run.py')

    parser.add_argument('--trade', dest='trade', action='store_const', const=True, default=False,
                        help='perform automatic FX trade')
    parser.add_argument('--algorithm_test', dest='algorithm_test', action='store_const', const=True, default=False,
                        help='perform algorithm test')
    parser.add_argument('--api_test', dest='api_test', action='store_const', const=True, default=False,
                        help='perform API test')
    parser.add_argument('--progress_view', dest='progress_view', action='store_const', const=True, default=False,
                        help='start progress viewer application')

    parser.add_argument('--progress_summary', dest='progress_summary', action='store_const', const=True, default=False,
                        help='show progress summary')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.algorithm_test:
        algorithm_test()

    if args.api_test:
        api_test()

    if args.trade:
        trade()

    if args.progress_view:
        progress_view(web=True)

    if args.progress_summary:
        progress_view(web=False)

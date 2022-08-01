"""
Serves as the entrypoint for each step.
"""
import argparse


def run_step():
    """
    Runs a step based on arguments received.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=str, default=True)
    args, _ = parser.parse_known_args()

    if args.step == 'preprocess':
        pass
    elif args.step == 'train':
        pass
    elif args.step == 'evaluate':
        pass

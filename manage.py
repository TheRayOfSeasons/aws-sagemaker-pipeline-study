import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--run', type=str, default=True)
args, _ = parser.parse_known_args()


if args.run == 'pipeline':
    from src.run_pipeline import run_pipeline
    run_pipeline()
elif args.run == 'step':
    from src.run_step import run_step
    run_step()

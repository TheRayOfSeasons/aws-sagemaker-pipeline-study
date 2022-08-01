import argparse
import pickle

import boto3

from src.ai.dataset import extract_dataset
from src.utils.logger import logger


parser = argparse.ArgumentParser()
parser.add_argument('--bucket_name', type=str, default=True)
parser.add_argument('--source_s3_path', type=str, default=True)
args, _ = parser.parse_known_args()


if __name__ == '__main__':
    filename = '/opt/ml/processing/train/data.csv'
    S3 = boto3.resource('s3')
    bucket = S3.Bucket(args.bucket_name)
    bucket.download_file(args.source_s3_path, filename)

    logger.info('Extracting dataset...')
    X, y = extract_dataset(filename)
    logger.info('Dataset extracted!')

    pickle.dump([X,y], open('/opt/ml/processing/train/data.pickle', 'wb'))

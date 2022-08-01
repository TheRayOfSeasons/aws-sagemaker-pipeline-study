import os
import sys
import traceback

import boto3
import sagemaker
from sagemaker.processing import ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

from src.settings import BASE_DIR
from src.settings import DATASET_DUMP_PATH
from src.utils.logger import logger


boto_session = boto3.Session(region_name='ap-southeast-1')
sagemaker_client = boto_session.client('sagemaker')
runtime_client = boto_session.client('sagemaker-runtime')

sagemaker_session = sagemaker.session.Session(
    boto_session=boto_session,
    sagemaker_client=sagemaker_client,
    sagemaker_runtime_client=runtime_client,
)

S3 = boto_session.resource('s3')
BUCKET_NAME = 'sagemaker-learning-bucket-5678'
BUCKET = S3.Bucket(BUCKET_NAME)


def get_pipeline():
    """
    Configures and returns the pipeline.
    """

    role = sagemaker.session.get_execution_role(sagemaker_session)

    music_data_object_path = 'rawdata/music.csv'
    BUCKET.Object(music_data_object_path).upload_file(DATASET_DUMP_PATH)

    sklearn_processor = SKLearnProcessor(
        framework_version='0.23-1',
        instance_type='ml.m5.large',
        instance_count=1,
        base_job_name='job-preprocess', # give better name
        sagemaker_session=sagemaker_session,
        role=role,
    )
    step_args = sklearn_processor.run(
        code=os.path.join(BASE_DIR, 'manage.py'),
        outputs=[
            ProcessingOutput(
                output_name='train',
                source='/opt/ml/processing/train'
            ),
        ],
        arguments=[
            '--run', 'step'
            '--step', 'preprocess',
            '--bucket_name', BUCKET_NAME,
            '--source_s3_path', music_data_object_path
        ]
    )
    preprocessing_step = ProcessingStep(
        name='PreprocessMusicData',
        step_args=step_args
    )

    pipeline = Pipeline(
        name='Sample Pipeline',
        parameters=[],
        steps=[
            preprocessing_step
        ],
        sagemaker_session=sagemaker_session
    )
    return pipeline


def run_pipeline():
    """
    Runs the pipeline.
    """

    try:
        pipeline = get_pipeline()
        execution = pipeline.start()
        execution.wait(max_attempts=120, delay=60)
        logger.info('Success!')
    except Exception as e:
        logger.info(f'Exception: {e}')
        traceback.print_exc()
        sys,exit(1)

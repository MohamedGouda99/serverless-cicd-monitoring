import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda function to deploy application from CodePipeline artifacts
    """
    try:
        logger.info("Starting deployment process")
        logger.info(f"Event: {json.dumps(event)}")
        
        # Extract artifact information from CodePipeline event
        codepipeline = boto3.client('codepipeline')
        job_id = event['CodePipeline.job']['id']
        
        try:
            # Get job details
            job_details = codepipeline.get_job_details(jobId=job_id)
            logger.info(f"Job details: {json.dumps(job_details)}")
            
            # Extract input artifacts
            input_artifacts = event['CodePipeline.job']['data']['inputArtifacts']
            
            for artifact in input_artifacts:
                artifact_location = artifact['location']['s3Location']
                bucket = artifact_location['bucketName']
                key = artifact_location['objectKey']
                
                logger.info(f"Processing artifact: s3://{bucket}/{key}")
                
                # Download artifact from S3
                response = s3_client.get_object(Bucket=bucket, Key=key)
                artifact_data = response['Body'].read()
                
                logger.info(f"Downloaded artifact: {len(artifact_data)} bytes")
                
                # Here you would typically:
                # 1. Extract the deployment package
                # 2. Update Lambda function code
                # 3. Update other services
                # 4. Run health checks
                
                logger.info("Deployment completed successfully")
            
            # Signal success to CodePipeline
            codepipeline.put_job_success_result(jobId=job_id)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Deployment completed successfully',
                    'jobId': job_id
                })
            }
            
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}")
            codepipeline.put_job_failure_result(
                jobId=job_id,
                failureDetails={
                    'type': 'JobFailed',
                    'message': str(e)
                }
            )
            raise
            
    except Exception as e:
        logger.error(f"Error in deployment function: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


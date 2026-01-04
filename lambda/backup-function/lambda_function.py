import json
import boto3
import os
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    """
    Lambda function for automated backup operations
    """
    try:
        logger.info("Starting backup process")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        backup_bucket = os.getenv('BACKUP_BUCKET', 'backup-bucket')
        
        # Example: Backup DynamoDB tables
        tables_to_backup = os.getenv('TABLES_TO_BACKUP', '').split(',')
        
        backup_results = []
        
        for table_name in tables_to_backup:
            if not table_name.strip():
                continue
                
            try:
                logger.info(f"Backing up table: {table_name}")
                
                # Export table data (simplified example)
                # In production, use DynamoDB Streams or AWS Backup
                response = dynamodb_client.scan(TableName=table_name.strip())
                
                # Save to S3
                backup_key = f"backups/{table_name}/{timestamp}.json"
                s3_client.put_object(
                    Bucket=backup_bucket,
                    Key=backup_key,
                    Body=json.dumps(response['Items'], default=str),
                    ServerSideEncryption='AES256'
                )
                
                backup_results.append({
                    'table': table_name,
                    'status': 'success',
                    'backup_location': f"s3://{backup_bucket}/{backup_key}"
                })
                
                logger.info(f"Backup completed for {table_name}")
                
            except Exception as e:
                logger.error(f"Failed to backup {table_name}: {str(e)}")
                backup_results.append({
                    'table': table_name,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Backup process completed',
                'timestamp': timestamp,
                'results': backup_results
            })
        }
        
    except Exception as e:
        logger.error(f"Error in backup function: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


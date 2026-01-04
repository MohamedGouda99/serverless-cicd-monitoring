import json
import boto3
import os
import logging
import requests

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

sns_client = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Lambda function for health checks and monitoring
    """
    try:
        logger.info("Starting monitoring checks")
        
        sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
        checks = []
        
        # Check 1: Lambda function health
        functions_to_check = os.getenv('FUNCTIONS_TO_MONITOR', '').split(',')
        
        for function_name in functions_to_check:
            if not function_name.strip():
                continue
                
            try:
                response = lambda_client.get_function(FunctionName=function_name.strip())
                status = response['Configuration']['State']
                
                checks.append({
                    'check': f'Lambda-{function_name}',
                    'status': 'healthy' if status == 'Active' else 'unhealthy',
                    'details': status
                })
                
                if status != 'Active':
                    send_alert(sns_topic_arn, f"Lambda function {function_name} is not active: {status}")
                    
            except Exception as e:
                logger.error(f"Error checking {function_name}: {str(e)}")
                checks.append({
                    'check': f'Lambda-{function_name}',
                    'status': 'error',
                    'error': str(e)
                })
                send_alert(sns_topic_arn, f"Error checking Lambda function {function_name}: {str(e)}")
        
        # Check 2: Application endpoint health
        endpoint_url = os.getenv('HEALTH_CHECK_URL', '')
        if endpoint_url:
            try:
                response = requests.get(endpoint_url, timeout=10)
                is_healthy = response.status_code == 200
                
                checks.append({
                    'check': 'Application-Endpoint',
                    'status': 'healthy' if is_healthy else 'unhealthy',
                    'status_code': response.status_code
                })
                
                if not is_healthy:
                    send_alert(sns_topic_arn, f"Application endpoint returned status {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error checking endpoint: {str(e)}")
                checks.append({
                    'check': 'Application-Endpoint',
                    'status': 'error',
                    'error': str(e)
                })
                send_alert(sns_topic_arn, f"Error checking application endpoint: {str(e)}")
        
        # Publish custom metric
        healthy_checks = sum(1 for c in checks if c.get('status') == 'healthy')
        total_checks = len(checks)
        
        cloudwatch.put_metric_data(
            Namespace='Custom/Monitoring',
            MetricData=[
                {
                    'MetricName': 'HealthCheckSuccessRate',
                    'Value': (healthy_checks / total_checks * 100) if total_checks > 0 else 0,
                    'Unit': 'Percent'
                }
            ]
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Monitoring checks completed',
                'checks': checks,
                'summary': {
                    'total': total_checks,
                    'healthy': healthy_checks,
                    'unhealthy': total_checks - healthy_checks
                }
            })
        }
        
    except Exception as e:
        logger.error(f"Error in monitoring function: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def send_alert(sns_topic_arn, message):
    """Send alert via SNS"""
    if sns_topic_arn:
        try:
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject='Monitoring Alert',
                Message=message
            )
            logger.info(f"Alert sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}")


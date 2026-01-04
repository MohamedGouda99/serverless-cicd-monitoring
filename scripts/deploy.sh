#!/bin/bash

set -e

echo "🚀 Deploying Lambda functions..."

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured."
    exit 1
fi

# Get bucket name from Terraform output
BUCKET=$(cd infrastructure && terraform output -raw lambda_deployments_bucket 2>/dev/null || echo "")

if [ -z "$BUCKET" ]; then
    echo "❌ Could not find deployment bucket. Please run terraform apply first."
    exit 1
fi

# Package and deploy each function
for func in deploy-function backup-function monitoring-function; do
    echo "📦 Packaging $func..."
    cd "lambda/$func"
    
    # Create deployment package
    pip install -r requirements.txt -t . --quiet
    zip -r "../../${func}.zip" . -x "*.pyc" "__pycache__/*" "tests/*" "*.git*" > /dev/null
    
    # Upload to S3
    echo "📤 Uploading $func to S3..."
    aws s3 cp "../../${func}.zip" "s3://$BUCKET/${func}.zip"
    
    # Update Lambda function
    echo "🔄 Updating Lambda function..."
    aws lambda update-function-code \
      --function-name "serverless-cicd-${func}" \
      --s3-bucket "$BUCKET" \
      --s3-key "${func}.zip" \
      --no-cli-pager
    
    cd ../..
done

echo "✅ Deployment complete!"


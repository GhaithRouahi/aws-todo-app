#!/bin/bash
set -e

# This script deploys the AWS SAM application.

# 1. Validate the SAM template
# This command checks if the SAM template is valid.
echo "Validating SAM template..."
sam validate --template-file deployment/sam/template.yaml

# 2. Build the project
# This command builds the Lambda functions and prepares them for deployment.
# The --use-container flag ensures the build happens in a Docker container
# that mimics the Lambda execution environment.
echo "Building SAM application..."
sam build --use-container

# 3. Deploy the project
# This command deploys the application to AWS CloudFormation.
# --guided is used for the first deployment to set up the configuration.
# Subsequent deployments will use the generated samconfig.toml file.
echo "Deploying SAM application..."
sam deploy --guided

# 4. Print the API Gateway endpoint URL
# This command retrieves the API endpoint URL from the stack outputs.
echo "Retrieving API Gateway endpoint URL..."
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name serverless-todo-api \
    --query "Stacks[0].Outputs[?OutputKey=='TodoApiEndpoint'].OutputValue" \
    --output text)

echo "--------------------------------------------------"
echo "Deployment complete!"
echo "API Gateway Endpoint URL: $API_ENDPOINT"
echo "--------------------------------------------------"

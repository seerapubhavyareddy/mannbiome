#!/bin/bash

# MannBiome Customer Portal V2 - Backend Deployment Script
# AWS ECR and App Runner Deployment

# AWS Configuration
AWS_REGION="us-east-2"
AWS_ACCOUNT_ID="088462465887"
REPOSITORY_NAME="mannbiome-portal-v2-backend"
IMAGE_TAG="latest"
APP_RUNNER_SERVICE_NAME="mannbiome-portal-v2-api"
IAM_ROLE_NAME="AppRunnerECRAccessRole-v2"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Derived variables
REPOSITORY_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPOSITORY_NAME"
ECR_REGISTRY_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}MannBiome Customer Portal V2 Backend${NC}"
echo -e "${BLUE}AWS Deployment Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo -e "${BLUE}  Region: $AWS_REGION${NC}"
echo -e "${BLUE}  Account ID: $AWS_ACCOUNT_ID${NC}"
echo -e "${BLUE}  Repository: $REPOSITORY_NAME${NC}"
echo -e "${BLUE}  Service: $APP_RUNNER_SERVICE_NAME${NC}"
echo ""

# Prerequisites check
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    # Check Docker
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}  Docker: Running${NC}"
    
    # Check AWS CLI
    if ! aws sts get-caller-identity > /dev/null 2>&1; then
        echo -e "${RED}AWS CLI is not configured. Please run 'aws configure' first.${NC}"
        exit 1
    fi
    echo -e "${GREEN}  AWS CLI: Configured${NC}"
    
    # Check required files
    if [ ! -f "dockerfile" ]; then
        echo -e "${RED}dockerfile not found in current directory${NC}"
        exit 1
    fi
    echo -e "${GREEN}  Dockerfile: Found${NC}"
    
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}requirements.txt not found in current directory${NC}"
        exit 1
    fi
    echo -e "${GREEN}  requirements.txt: Found${NC}"
    
    echo -e "${GREEN}All prerequisites met!${NC}"
    echo ""
}

# Create or verify ECR repository
setup_ecr_repository() {
    echo -e "${YELLOW}Step 1: Setting up ECR repository...${NC}"
    
    if ! aws ecr describe-repositories --repository-names "$REPOSITORY_NAME" --region "$AWS_REGION" > /dev/null 2>&1; then
        echo -e "${YELLOW}Creating ECR repository: $REPOSITORY_NAME${NC}"
        aws ecr create-repository \
            --repository-name "$REPOSITORY_NAME" \
            --region "$AWS_REGION" \
            --image-scanning-configuration scanOnPush=true \
            --encryption-configuration encryptionType=AES256
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}ECR repository created successfully${NC}"
        else
            echo -e "${RED}Failed to create ECR repository${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}ECR repository already exists${NC}"
    fi
    echo ""
}

# Login to ECR
login_to_ecr() {
    echo -e "${YELLOW}Step 2: Logging into ECR...${NC}"
    
    aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_REGISTRY_URI"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully logged into ECR${NC}"
    else
        echo -e "${RED}Failed to login to ECR${NC}"
        exit 1
    fi
    echo ""
}

# Build Docker image
build_docker_image() {
    echo -e "${YELLOW}Step 3: Building Docker image...${NC}"
    
    docker build -t "$REPOSITORY_NAME:$IMAGE_TAG" .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Docker image built successfully${NC}"
        
        # Show image size
        IMAGE_SIZE=$(docker images "$REPOSITORY_NAME:$IMAGE_TAG" --format "{{.Size}}")
        echo -e "${BLUE}  Image size: $IMAGE_SIZE${NC}"
    else
        echo -e "${RED}Failed to build Docker image${NC}"
        exit 1
    fi
    echo ""
}

# Tag Docker image
tag_docker_image() {
    echo -e "${YELLOW}Step 4: Tagging Docker image...${NC}"
    
    TIMESTAMP_TAG="production-$(date +%Y%m%d-%H%M%S)"
    
    docker tag "$REPOSITORY_NAME:$IMAGE_TAG" "$REPOSITORY_URI:$IMAGE_TAG"
    docker tag "$REPOSITORY_NAME:$IMAGE_TAG" "$REPOSITORY_URI:$TIMESTAMP_TAG"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Image tagged successfully${NC}"
        echo -e "${BLUE}  Tags: latest, $TIMESTAMP_TAG${NC}"
    else
        echo -e "${RED}Failed to tag image${NC}"
        exit 1
    fi
    echo ""
}

# Push image to ECR
push_to_ecr() {
    echo -e "${YELLOW}Step 5: Pushing image to ECR...${NC}"
    
    echo -e "${BLUE}Pushing latest tag...${NC}"
    docker push "$REPOSITORY_URI:$IMAGE_TAG"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Latest tag pushed successfully${NC}"
    else
        echo -e "${RED}Failed to push latest tag${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Pushing timestamp tag...${NC}"
    docker push "$REPOSITORY_URI:$TIMESTAMP_TAG"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Timestamp tag pushed successfully${NC}"
    else
        echo -e "${YELLOW}Warning: Timestamp tag push failed (non-critical)${NC}"
    fi
    echo ""
}

# Create IAM role for App Runner (only if it doesn't exist)
create_apprunner_iam_role() {
    echo -e "${YELLOW}Step 6: Setting up IAM role for App Runner...${NC}"
    
    # Check if role already exists
    if aws iam get-role --role-name "$IAM_ROLE_NAME" > /dev/null 2>&1; then
        echo -e "${GREEN}IAM role already exists: $IAM_ROLE_NAME${NC}"
    else
        echo -e "${YELLOW}Creating IAM role: $IAM_ROLE_NAME${NC}"
        
        # Create trust policy document
        cat > /tmp/apprunner-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "build.apprunner.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
        
        # Create the IAM role
        aws iam create-role \
            --role-name "$IAM_ROLE_NAME" \
            --assume-role-policy-document file:///tmp/apprunner-trust-policy.json \
            --description "Allows App Runner to access ECR for MannBiome Portal V2" > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}IAM role created successfully${NC}"
            
            # Attach the AWS managed policy for ECR access
            aws iam attach-role-policy \
                --role-name "$IAM_ROLE_NAME" \
                --policy-arn "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
            
            echo -e "${GREEN}ECR access policy attached${NC}"
            
            # Wait for IAM role to propagate
            echo -e "${BLUE}Waiting for IAM role to propagate...${NC}"
            sleep 10
        else
            echo -e "${RED}Failed to create IAM role${NC}"
            rm /tmp/apprunner-trust-policy.json
            exit 1
        fi
        
        # Clean up temp file
        rm /tmp/apprunner-trust-policy.json
    fi
    
    # Get the role ARN
    ROLE_ARN=$(aws iam get-role --role-name "$IAM_ROLE_NAME" --query 'Role.Arn' --output text)
    echo -e "${BLUE}  Role ARN: $ROLE_ARN${NC}"
    echo ""
}

# Deploy to App Runner
deploy_to_apprunner() {
    echo -e "${YELLOW}Step 7: Deploying to AWS App Runner...${NC}"
    
    # Check if service already exists
    EXISTING_SERVICE=$(aws apprunner list-services --region "$AWS_REGION" \
        --query "ServiceSummaryList[?ServiceName=='$APP_RUNNER_SERVICE_NAME'].ServiceArn" \
        --output text 2>/dev/null)
    
    if [ -z "$EXISTING_SERVICE" ]; then
        echo -e "${YELLOW}Creating new App Runner service...${NC}"
        
        # Create new service with authentication configuration
        SERVICE_OUTPUT=$(aws apprunner create-service \
            --service-name "$APP_RUNNER_SERVICE_NAME" \
            --source-configuration "{
                \"AuthenticationConfiguration\": {
                    \"AccessRoleArn\": \"$ROLE_ARN\"
                },
                \"ImageRepository\": {
                    \"ImageIdentifier\": \"$REPOSITORY_URI:$IMAGE_TAG\",
                    \"ImageRepositoryType\": \"ECR\",
                    \"ImageConfiguration\": {
                        \"Port\": \"8001\"
                    }
                },
                \"AutoDeploymentsEnabled\": true
            }" \
            --instance-configuration "{
                \"Cpu\": \"1 vCPU\",
                \"Memory\": \"2 GB\"
            }" \
            --region "$AWS_REGION" 2>&1)
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}App Runner service created successfully${NC}"
            SERVICE_ARN=$(echo "$SERVICE_OUTPUT" | grep -o '"ServiceArn": "[^"]*"' | cut -d'"' -f4)
        else
            echo -e "${RED}Failed to create App Runner service${NC}"
            echo "$SERVICE_OUTPUT"
            exit 1
        fi
    else
        echo -e "${YELLOW}Updating existing App Runner service...${NC}"
        
        # Update existing service
        aws apprunner update-service \
            --service-arn "$EXISTING_SERVICE" \
            --source-configuration "{
                \"AuthenticationConfiguration\": {
                    \"AccessRoleArn\": \"$ROLE_ARN\"
                },
                \"ImageRepository\": {
                    \"ImageIdentifier\": \"$REPOSITORY_URI:$IMAGE_TAG\",
                    \"ImageRepositoryType\": \"ECR\",
                    \"ImageConfiguration\": {
                        \"Port\": \"8001\"
                    }
                },
                \"AutoDeploymentsEnabled\": true
            }" \
            --region "$AWS_REGION"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}App Runner service updated successfully${NC}"
            SERVICE_ARN="$EXISTING_SERVICE"
        else
            echo -e "${RED}Failed to update App Runner service${NC}"
            exit 1
        fi
    fi
    
    echo -e "${BLUE}Service ARN: $SERVICE_ARN${NC}"
    echo ""
}

# Get service URL
get_service_url() {
    echo -e "${YELLOW}Step 8: Retrieving service URL...${NC}"
    echo -e "${BLUE}Waiting for service to be ready...${NC}"
    
    # Wait for service to be running
    sleep 5
    
    SERVICE_URL=$(aws apprunner describe-service \
        --service-arn "$SERVICE_ARN" \
        --region "$AWS_REGION" \
        --query 'Service.ServiceUrl' \
        --output text 2>/dev/null)
    
    if [ ! -z "$SERVICE_URL" ]; then
        echo -e "${GREEN}Service URL retrieved successfully${NC}"
        echo -e "${BLUE}  URL: https://$SERVICE_URL${NC}"
    else
        echo -e "${YELLOW}Could not retrieve service URL automatically${NC}"
        echo -e "${YELLOW}Check AWS Console for the service URL${NC}"
    fi
    echo ""
}

# Display summary
display_summary() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Completed Successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Deployment Summary:${NC}"
    echo -e "${BLUE}  ECR Repository: $REPOSITORY_URI${NC}"
    echo -e "${BLUE}  Image Tag: $IMAGE_TAG${NC}"
    echo -e "${BLUE}  App Runner Service: $APP_RUNNER_SERVICE_NAME${NC}"
    echo -e "${BLUE}  IAM Role: $IAM_ROLE_NAME${NC}"
    
    if [ ! -z "$SERVICE_URL" ]; then
        echo -e "${BLUE}  Backend URL: https://$SERVICE_URL${NC}"
        echo ""
        echo -e "${YELLOW}Next Steps:${NC}"
        echo -e "1. Test your backend API: ${BLUE}https://$SERVICE_URL/api/health-check${NC}"
        echo -e "2. Update your frontend with this backend URL"
        echo -e "3. Redeploy frontend with new backend URL"
        echo ""
        echo -e "${YELLOW}Frontend Redeploy Commands:${NC}"
        echo -e "${BLUE}export REACT_APP_API_BASE_URL=\"https://$SERVICE_URL\"${NC}"
        echo -e "${BLUE}echo \"REACT_APP_API_BASE_URL=https://$SERVICE_URL\" > .env.production${NC}"
        echo -e "${BLUE}npm run build${NC}"
        echo -e "${BLUE}aws s3 sync build/ s3://mannbiome-portal-v2-frontend-088462465887 --delete --region us-east-2${NC}"
        echo -e "${BLUE}aws cloudfront create-invalidation --distribution-id EL01U982VXK57 --paths \"/*\"${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}Useful Commands:${NC}"
    echo -e "  View ECR images: ${BLUE}aws ecr list-images --repository-name $REPOSITORY_NAME --region $AWS_REGION${NC}"
    echo -e "  View App Runner service: ${BLUE}aws apprunner describe-service --service-arn $SERVICE_ARN --region $AWS_REGION${NC}"
    echo -e "  Update service: Re-run this script"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_ecr_repository
    login_to_ecr
    build_docker_image
    tag_docker_image
    push_to_ecr
    create_apprunner_iam_role
    deploy_to_apprunner
    get_service_url
    display_summary
}

# Run the deployment
main "$@"
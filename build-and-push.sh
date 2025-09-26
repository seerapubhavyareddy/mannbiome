#!/bin/bash

# AWS ECR Configuration
AWS_REGION="us-east-2"  # Change to your preferred region
AWS_ACCOUNT_ID="088462465887"  # Your AWS account ID
REPOSITORY_NAME="mannbiome-customer-portal-api"
IMAGE_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get AWS Account ID automatically if not set
if [ "$AWS_ACCOUNT_ID" = "088462465887" ]; then
    echo -e "${GREEN}Using configured AWS Account ID: $AWS_ACCOUNT_ID${NC}"
else
    echo -e "${YELLOW}Getting AWS Account ID...${NC}"
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo -e "${GREEN}AWS Account ID: $AWS_ACCOUNT_ID${NC}"
fi

REPOSITORY_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPOSITORY_NAME"
ECR_REGISTRY_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

echo -e "${BLUE}Starting MannBiome Customer Portal API deployment...${NC}"
echo -e "${BLUE}Region: $AWS_REGION${NC}"
echo -e "${BLUE}Repository: $REPOSITORY_NAME${NC}"
echo -e "${BLUE}Image Tag: $IMAGE_TAG${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}AWS CLI is not configured. Please run 'aws configure' first.${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Checking if ECR repository exists...${NC}"

# Check if repository exists, create if it doesn't
if ! aws ecr describe-repositories --repository-names "$REPOSITORY_NAME" --region "$AWS_REGION" > /dev/null 2>&1; then
    echo -e "${YELLOW}Creating ECR repository: $REPOSITORY_NAME${NC}"
    aws ecr create-repository \
        --repository-name "$REPOSITORY_NAME" \
        --region "$AWS_REGION" \
        --image-scanning-configuration scanOnPush=true
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}ECR repository created successfully!${NC}"
    else
        echo -e "${RED}Failed to create ECR repository${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}ECR repository already exists${NC}"
fi

echo -e "${YELLOW}Step 2: Logging into ECR...${NC}"

# Get ECR login token and login to Docker - FIXED
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_REGISTRY_URI"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully logged into ECR${NC}"
else
    echo -e "${RED}Failed to login to ECR${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 3: Building Docker image...${NC}"

# Build the Docker image
docker build -t "$REPOSITORY_NAME:$IMAGE_TAG" .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Docker image built successfully${NC}"
else
    echo -e "${RED}Failed to build Docker image${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 4: Tagging image for ECR...${NC}"

# Tag the image for ECR
TIMESTAMP_TAG="production-$(date +%Y%m%d-%H%M%S)"
docker tag "$REPOSITORY_NAME:$IMAGE_TAG" "$REPOSITORY_URI:$IMAGE_TAG"
docker tag "$REPOSITORY_NAME:$IMAGE_TAG" "$REPOSITORY_URI:$TIMESTAMP_TAG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Image tagged successfully${NC}"
    echo -e "${BLUE}Tags created: $IMAGE_TAG, $TIMESTAMP_TAG${NC}"
else
    echo -e "${RED}Failed to tag image${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 5: Pushing image to ECR...${NC}"

# Push the latest tag first
echo -e "${BLUE}Pushing latest tag...${NC}"
docker push "$REPOSITORY_URI:$IMAGE_TAG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Latest tag pushed successfully${NC}"
else
    echo -e "${RED}Failed to push latest tag${NC}"
    exit 1
fi

# Push the timestamp tag
echo -e "${BLUE}Pushing timestamp tag: $TIMESTAMP_TAG${NC}"
docker push "$REPOSITORY_URI:$TIMESTAMP_TAG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Timestamp tag pushed successfully${NC}"
else
    echo -e "${YELLOW}Warning: Failed to push timestamp tag, but latest tag was successful${NC}"
    echo -e "${YELLOW}This is not critical - you can still deploy with the latest tag${NC}"
fi

echo ""
echo -e "${GREEN}Deployment preparation completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Create an ECS service using this image"
echo -e "2. Or deploy to AWS App Runner using this image URI"
echo -e "3. Image URI for deployment: ${GREEN}$REPOSITORY_URI:$IMAGE_TAG${NC}"
echo -e "4. Your MannBiome Customer Portal API is ready to deploy!"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo -e "   View repository: aws ecr describe-repositories --repository-names $REPOSITORY_NAME --region $AWS_REGION"
echo -e "   List images: aws ecr list-images --repository-name $REPOSITORY_NAME --region $AWS_REGION"
echo ""
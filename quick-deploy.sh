#!/bin/bash

# Quick deployment script for MannBiome Customer Portal API
# Account ID: 088462465887

echo "🚀 Quick Deploy Script for MannBiome Customer Portal API"
echo "Account ID: 088462465887"
echo "Region: us-east-2"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
AWS_ACCOUNT_ID="088462465887"
AWS_REGION="us-east-2"
REPOSITORY_NAME="mannbiome-customer-portal-api"
CLUSTER_NAME="mannbiome-customer-portal-cluster"
SERVICE_NAME="mannbiome-customer-portal-api-service"

echo -e "${BLUE}📋 Pre-deployment Checklist:${NC}"
echo "✅ AWS CLI configured"
echo "✅ Docker installed and running"
echo "✅ Account ID: $AWS_ACCOUNT_ID"
echo "✅ Region: $AWS_REGION"
echo ""

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI first.${NC}"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity > /dev/null 2>&1; then
        echo -e "${RED}❌ AWS credentials not configured. Please run 'aws configure' first.${NC}"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker daemon not running. Please start Docker first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All prerequisites met!${NC}"
}

# Function to create ECR repository
create_ecr_repository() {
    echo -e "${YELLOW}📦 Step 1: Creating ECR repository...${NC}"
    
    if aws ecr describe-repositories --repository-names "$REPOSITORY_NAME" --region "$AWS_REGION" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ ECR repository already exists${NC}"
    else
        aws ecr create-repository \
            --repository-name "$REPOSITORY_NAME" \
            --region "$AWS_REGION" \
            --image-scanning-configuration scanOnPush=true
        echo -e "${GREEN}✅ ECR repository created successfully!${NC}"
    fi
}

# Function to create ECS cluster
create_ecs_cluster() {
    echo -e "${YELLOW}🏗️  Step 2: Creating ECS cluster...${NC}"
    
    if aws ecs describe-clusters --clusters "$CLUSTER_NAME" --region "$AWS_REGION" --query 'clusters[0].status' --output text 2>/dev/null | grep -q "ACTIVE"; then
        echo -e "${GREEN}✅ ECS cluster already exists${NC}"
    else
        aws ecs create-cluster \
            --cluster-name "$CLUSTER_NAME" \
            --capacity-providers FARGATE \
            --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
            --region "$AWS_REGION"
        echo -e "${GREEN}✅ ECS cluster created successfully!${NC}"
    fi
}

# Function to create CloudWatch log group
create_log_group() {
    echo -e "${YELLOW}📊 Step 3: Creating CloudWatch log group...${NC}"
    
    if aws logs describe-log-groups --log-group-name-prefix "/ecs/mannbiome-customer-portal-api" --region "$AWS_REGION" --query 'logGroups[0].logGroupName' --output text 2>/dev/null | grep -q "/ecs/mannbiome-customer-portal-api"; then
        echo -e "${GREEN}✅ CloudWatch log group already exists${NC}"
    else
        aws logs create-log-group \
            --log-group-name "/ecs/mannbiome-customer-portal-api" \
            --region "$AWS_REGION"
        echo -e "${GREEN}✅ CloudWatch log group created successfully!${NC}"
    fi
}

# Function to build and push image
build_and_push() {
    echo -e "${YELLOW}🔨 Step 4: Building and pushing Docker image...${NC}"
    
    # Make build script executable and run it
    chmod +x build-and-push.sh
    ./build-and-push.sh
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Image built and pushed successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to build and push image${NC}"
        exit 1
    fi
}

# Function to create or update ECS task definition
create_task_definition() {
    echo -e "${YELLOW}📋 Step 5: Creating ECS task definition...${NC}"
    
    aws ecs register-task-definition \
        --cli-input-json file://ecs-task-definition.json \
        --region "$AWS_REGION"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ ECS task definition created successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to create ECS task definition${NC}"
        exit 1
    fi
}

# Main deployment function
main() {
    echo -e "${BLUE}🚀 Starting MannBiome Customer Portal API deployment preparation...${NC}"
    echo ""
    
    check_prerequisites
    create_ecr_repository
    create_ecs_cluster
    create_log_group
    build_and_push
    create_task_definition
    
    echo ""
    echo -e "${GREEN}🎉 Deployment preparation completed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}🔗 Next Steps - Choose your deployment option:${NC}"
    echo ""
    echo -e "${BLUE}Option A: AWS App Runner (Recommended for simplicity)${NC}"
    echo "1. Go to AWS Console → App Runner"
    echo "2. Create service from container image"
    echo "3. Use image URI: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPOSITORY_NAME:latest"
    echo "4. Configure port: 8001"
    echo "5. Add environment variables from .env.example"
    echo ""
    echo -e "${BLUE}Option B: ECS Fargate (More control)${NC}"
    echo "1. Create ECS service using the task definition"
    echo "2. Create Application Load Balancer"
    echo "3. Configure target groups and security groups"
    echo ""
    echo -e "${YELLOW}📊 Resources Created:${NC}"
    echo "• ECR Repository: $REPOSITORY_NAME"
    echo "• ECS Cluster: $CLUSTER_NAME"
    echo "• CloudWatch Log Group: /ecs/mannbiome-customer-portal-api"
    echo "• Task Definition: mannbiome-customer-portal-api-task"
    echo ""
    echo -e "${GREEN}🔗 Your MannBiome Customer Portal API is ready to deploy!${NC}"
}

# Run the deployment preparation
main "$@"
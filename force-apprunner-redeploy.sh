#!/bin/bash

# Force App Runner re-deployment for MannBiome Customer Portal API
echo "🔄 Forcing App Runner re-deployment..."

# Configuration - update these if different
AWS_REGION="us-east-2"
AWS_ACCOUNT_ID="088462465887"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🔍 Step 1: Finding your App Runner service...${NC}"

# List all App Runner services
echo "Available App Runner services:"
aws apprunner list-services --region $AWS_REGION --query 'ServiceSummaryList[].{Name:ServiceName,Status:Status,Arn:ServiceArn}' --output table

echo ""
echo -e "${YELLOW}Please select your service (likely contains 'mannbiome' or 'customer-portal'):${NC}"
read -p "Enter the exact service name: " SERVICE_NAME

if [ -z "$SERVICE_NAME" ]; then
    echo -e "${RED}❌ Service name is required${NC}"
    exit 1
fi

# Get service ARN
SERVICE_ARN=$(aws apprunner list-services --region $AWS_REGION --query "ServiceSummaryList[?ServiceName=='$SERVICE_NAME'].ServiceArn" --output text)

if [ -z "$SERVICE_ARN" ] || [ "$SERVICE_ARN" = "None" ]; then
    echo -e "${RED}❌ Service '$SERVICE_NAME' not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found service: $SERVICE_NAME${NC}"
echo -e "${BLUE}📋 Service ARN: $SERVICE_ARN${NC}"

echo -e "${YELLOW}🚀 Step 2: Starting deployment...${NC}"

# Start deployment
DEPLOYMENT_ID=$(aws apprunner start-deployment \
    --service-arn "$SERVICE_ARN" \
    --region $AWS_REGION \
    --query 'OperationId' \
    --output text 2>/dev/null)

if [ $? -eq 0 ] && [ ! -z "$DEPLOYMENT_ID" ]; then
    echo -e "${GREEN}✅ Deployment started successfully!${NC}"
    echo -e "${BLUE}📋 Deployment ID: $DEPLOYMENT_ID${NC}"
else
    echo -e "${RED}❌ Failed to start deployment. Trying alternative method...${NC}"
    
    # Alternative: Update service configuration to force redeploy
    echo -e "${YELLOW}🔄 Attempting service update to force redeploy...${NC}"
    
    # Get current service configuration
    aws apprunner describe-service \
        --service-arn "$SERVICE_ARN" \
        --region $AWS_REGION \
        --query 'Service.SourceConfiguration' > current-config.json
    
    # Trigger update (this will force a new deployment)
    aws apprunner update-service \
        --service-arn "$SERVICE_ARN" \
        --source-configuration file://current-config.json \
        --region $AWS_REGION > /dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Service update initiated - this will trigger a new deployment${NC}"
        rm current-config.json
    else
        echo -e "${RED}❌ Failed to update service${NC}"
        rm current-config.json
        exit 1
    fi
fi

echo -e "${YELLOW}📊 Step 3: Monitoring deployment status...${NC}"
echo -e "${BLUE}This may take 5-10 minutes...${NC}"

# Monitor deployment
COUNTER=0
while [ $COUNTER -lt 20 ]; do
    STATUS=$(aws apprunner describe-service \
        --service-arn "$SERVICE_ARN" \
        --region $AWS_REGION \
        --query 'Service.Status' \
        --output text 2>/dev/null)
    
    echo -e "${BLUE}[$(date '+%H:%M:%S')] Current status: $STATUS${NC}"
    
    if [ "$STATUS" = "RUNNING" ]; then
        echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
        break
    elif [ "$STATUS" = "OPERATION_IN_PROGRESS" ]; then
        echo -e "${YELLOW}⏳ Deployment in progress... waiting 30 seconds${NC}"
        sleep 30
    elif [ "$STATUS" = "CREATE_FAILED" ] || [ "$STATUS" = "UPDATE_FAILED" ]; then
        echo -e "${RED}❌ Deployment failed with status: $STATUS${NC}"
        break
    else
        echo -e "${YELLOW}Status: $STATUS - waiting 30 seconds${NC}"
        sleep 30
    fi
    
    COUNTER=$((COUNTER + 1))
done

# Get the service URL
SERVICE_URL=$(aws apprunner describe-service \
    --service-arn "$SERVICE_ARN" \
    --region $AWS_REGION \
    --query 'Service.ServiceUrl' \
    --output text 2>/dev/null)

echo ""
echo -e "${GREEN}🎉 App Runner Deployment Process Complete!${NC}"
echo -e "${BLUE}🌐 Service URL: https://$SERVICE_URL${NC}"
echo -e "${BLUE}🔍 Health Check: https://$SERVICE_URL/api/health-check${NC}"
echo -e "${BLUE}📚 API Docs: https://$SERVICE_URL/docs${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Test your new report generation endpoints"
echo "2. Verify all API changes are working"
echo "3. Update and redeploy frontend if needed"
echo ""
echo -e "${YELLOW}🧪 Test your new report endpoint:${NC}"
echo "curl -X POST 'https://$SERVICE_URL/api/reports/generate' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"type\": \"full\", \"customer_id\": 3}' \\"
echo "  --output test-report.pdf"
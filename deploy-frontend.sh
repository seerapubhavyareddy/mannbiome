#!/bin/bash

# Frontend deployment script for MannBiome Customer Portal
# Account ID: 088462465887

echo "🌐 Frontend Deployment Script for MannBiome Customer Portal"
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
S3_BUCKET_NAME="mannbiome-customer-portal-frontend-${AWS_ACCOUNT_ID}"
CLOUDFRONT_COMMENT="MannBiome Customer Portal Frontend Distribution"

# Get the backend URL from user input
echo -e "${YELLOW}📝 Enter your backend API URL (from App Runner):${NC}"
echo "Example: https://abc123def.us-east-2.awsapprunner.com"
read -p "Backend URL: " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo -e "${RED}❌ Backend URL is required${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}🚀 Starting frontend deployment...${NC}"
echo -e "${BLUE}📍 S3 Bucket: $S3_BUCKET_NAME${NC}"
echo -e "${BLUE}🔗 Backend URL: $BACKEND_URL${NC}"
echo ""

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI first.${NC}"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ Node.js/npm not found. Please install Node.js first.${NC}"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity > /dev/null 2>&1; then
        echo -e "${RED}❌ AWS credentials not configured. Please run 'aws configure' first.${NC}"
        exit 1
    fi
    
    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        echo -e "${RED}❌ package.json not found. Please run this script from your React app directory.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All prerequisites met!${NC}"
}

# Function to create S3 bucket
create_s3_bucket() {
    echo -e "${YELLOW}🪣 Step 1: Creating S3 bucket...${NC}"
    
    if aws s3 ls "s3://$S3_BUCKET_NAME" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ S3 bucket already exists${NC}"
    else
        # Create bucket
        aws s3 mb "s3://$S3_BUCKET_NAME" --region "$AWS_REGION"
        
        # Configure for static website hosting
        aws s3 website "s3://$S3_BUCKET_NAME" \
            --index-document index.html \
            --error-document index.html
        
        # Set bucket policy for public read access
        cat > bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$S3_BUCKET_NAME/*"
        }
    ]
}
EOF
        
        aws s3api put-bucket-policy \
            --bucket "$S3_BUCKET_NAME" \
            --policy file://bucket-policy.json
        
        # Remove policy file
        rm bucket-policy.json
        
        echo -e "${GREEN}✅ S3 bucket created and configured for static hosting${NC}"
    fi
}

# Function to build React app
build_react_app() {
    echo -e "${YELLOW}🔨 Step 2: Building React application...${NC}"
    
    # Install dependencies
    echo "Installing dependencies..."
    npm install
    
    # Build the React app with the backend URL
    echo "Building React app with backend URL: $BACKEND_URL"
    REACT_APP_API_BASE_URL="$BACKEND_URL" npm run build
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ React app built successfully${NC}"
    else
        echo -e "${RED}❌ Failed to build React app${NC}"
        exit 1
    fi
}

# Function to deploy to S3
deploy_to_s3() {
    echo -e "${YELLOW}📤 Step 3: Deploying to S3...${NC}"
    
    # Upload build files to S3
    aws s3 sync build/ "s3://$S3_BUCKET_NAME" --delete --region "$AWS_REGION"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Files uploaded to S3 successfully${NC}"
    else
        echo -e "${RED}❌ Failed to upload files to S3${NC}"
        exit 1
    fi
}

# Function to create CloudFront distribution
create_cloudfront() {
    echo -e "${YELLOW}☁️  Step 4: Creating CloudFront distribution...${NC}"
    
    # Check if distribution already exists
    EXISTING_DISTRIBUTION=$(aws cloudfront list-distributions \
        --query "DistributionList.Items[?Origins.Items[?DomainName=='$S3_BUCKET_NAME.s3.amazonaws.com']].Id" \
        --output text 2>/dev/null)
    
    if [ ! -z "$EXISTING_DISTRIBUTION" ] && [ "$EXISTING_DISTRIBUTION" != "None" ]; then
        echo -e "${GREEN}✅ CloudFront distribution already exists: $EXISTING_DISTRIBUTION${NC}"
        DISTRIBUTION_ID="$EXISTING_DISTRIBUTION"
    else
        # Create CloudFront distribution config
        cat > cloudfront-config.json << EOF
{
    "CallerReference": "mannbiome-frontend-$(date +%s)",
    "Comment": "$CLOUDFRONT_COMMENT",
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3-$S3_BUCKET_NAME",
        "ViewerProtocolPolicy": "redirect-to-https",
        "MinTTL": 0,
        "ForwardedValues": {
            "QueryString": false,
            "Cookies": {
                "Forward": "none"
            }
        },
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        }
    },
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "S3-$S3_BUCKET_NAME",
                "DomainName": "$S3_BUCKET_NAME.s3.amazonaws.com",
                "S3OriginConfig": {
                    "OriginAccessIdentity": ""
                }
            }
        ]
    },
    "Enabled": true,
    "DefaultRootObject": "index.html",
    "CustomErrorResponses": {
        "Quantity": 2,
        "Items": [
            {
                "ErrorCode": 404,
                "ResponsePagePath": "/index.html",
                "ResponseCode": "200"
            },
            {
                "ErrorCode": 403,
                "ResponsePagePath": "/index.html", 
                "ResponseCode": "200"
            }
        ]
    },
    "PriceClass": "PriceClass_100"
}
EOF
        
        # Create distribution
        DISTRIBUTION_OUTPUT=$(aws cloudfront create-distribution \
            --distribution-config file://cloudfront-config.json \
            --region "$AWS_REGION")
        
        DISTRIBUTION_ID=$(echo "$DISTRIBUTION_OUTPUT" | grep -o '"Id": "[^"]*"' | head -1 | cut -d'"' -f4)
        DISTRIBUTION_DOMAIN=$(echo "$DISTRIBUTION_OUTPUT" | grep -o '"DomainName": "[^"]*"' | head -1 | cut -d'"' -f4)
        
        # Remove config file
        rm cloudfront-config.json
        
        echo -e "${GREEN}✅ CloudFront distribution created: $DISTRIBUTION_ID${NC}"
        echo -e "${YELLOW}⏳ Distribution is deploying... This may take 10-15 minutes${NC}"
    fi
}

# Function to invalidate CloudFront cache
invalidate_cloudfront() {
    if [ ! -z "$DISTRIBUTION_ID" ]; then
        echo -e "${YELLOW}🔄 Step 5: Invalidating CloudFront cache...${NC}"
        
        aws cloudfront create-invalidation \
            --distribution-id "$DISTRIBUTION_ID" \
            --paths "/*" \
            --region "$AWS_REGION" > /dev/null
        
        echo -e "${GREEN}✅ CloudFront cache invalidation initiated${NC}"
    fi
}

# Function to get website URLs
get_urls() {
    echo ""
    echo -e "${GREEN}🎉 Frontend deployment completed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Your application URLs:${NC}"
    echo -e "${BLUE}🌐 S3 Website URL:${NC} http://$S3_BUCKET_NAME.s3-website.us-east-2.amazonaws.com"
    
    if [ ! -z "$DISTRIBUTION_ID" ]; then
        CLOUDFRONT_URL=$(aws cloudfront get-distribution \
            --id "$DISTRIBUTION_ID" \
            --query 'Distribution.DomainName' \
            --output text 2>/dev/null)
        
        if [ ! -z "$CLOUDFRONT_URL" ] && [ "$CLOUDFRONT_URL" != "None" ]; then
            echo -e "${BLUE}☁️  CloudFront URL:${NC} https://$CLOUDFRONT_URL"
            echo -e "${GREEN}👆 Use the CloudFront URL for production (faster, global CDN)${NC}"
        fi
    fi
    
    echo ""
    echo -e "${YELLOW}🔗 Backend API URL:${NC} $BACKEND_URL"
    echo ""
    echo -e "${GREEN}✅ Your MannBiome Customer Portal is now live!${NC}"
}

# Main deployment function
main() {
    echo -e "${BLUE}🚀 Starting MannBiome Customer Portal frontend deployment...${NC}"
    echo ""
    
    check_prerequisites
    create_s3_bucket
    build_react_app
    deploy_to_s3
    create_cloudfront
    invalidate_cloudfront
    get_urls
    
    echo ""
    echo -e "${YELLOW}🛠️  Next steps:${NC}"
    echo "1. Test your frontend application"
    echo "2. Configure custom domain (optional)"
    echo "3. Set up SSL certificate with ACM (optional)"
    echo "4. Configure monitoring and analytics"
    echo ""
}

# Run the deployment
main "$@"
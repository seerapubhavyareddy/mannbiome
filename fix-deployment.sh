#!/bin/bash

# Complete fix for MannBiome Customer Portal deployment issues

echo "🔧 Fixing all deployment issues..."

# Configuration
BACKEND_URL="https://yd3weja3cp.us-east-2.awsapprunner.com"
S3_BUCKET="mannbiome-customer-portal-frontend-088462465887"
CLOUDFRONT_DISTRIBUTION_ID="E47LTJIFSM54C"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🔍 Step 1: Testing backend connectivity...${NC}"
if curl -s --fail "$BACKEND_URL/api/health-check" > /dev/null; then
    echo -e "${GREEN}✅ Backend is responding${NC}"
else
    echo -e "${RED}❌ Backend is not responding. Checking alternative endpoints...${NC}"
    
    # Try different endpoints
    if curl -s --fail "$BACKEND_URL/" > /dev/null; then
        echo -e "${YELLOW}⚠️  Backend root responds but /api/health-check doesn't exist${NC}"
        echo -e "${YELLOW}📝 You may need to update your FastAPI backend to include the missing endpoints${NC}"
    else
        echo -e "${RED}❌ Backend is completely down${NC}"
        echo -e "${YELLOW}📝 Please check your App Runner service status${NC}"
    fi
fi

echo -e "${YELLOW}📁 Step 2: Creating missing assets directories...${NC}"
mkdir -p public/assets/images/food_lifestyle
mkdir -p public/assets/images/probiotics_images

echo -e "${YELLOW}🖼️  Step 3: Creating placeholder images...${NC}"

# Food lifestyle images
cat > public/assets/images/food_lifestyle/oats.jpeg << 'EOF'
data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjcwIiB2aWV3Qm94PSIwIDAgMTAwIDcwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjcwIiBmaWxsPSIjMDBCRkE1Ii8+Cjx0ZXh0IHg9IjUwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSI+T2F0czwvdGV4dD4KPC9zdmc+
EOF

# Create a simple SVG placeholder for all missing images
create_placeholder() {
    local filename="$1"
    local text="$2"
    cat > "$filename" << EOF
<svg width="100" height="70" viewBox="0 0 100 70" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="70" fill="#00BFA5"/>
<text x="50" y="35" font-family="Arial" font-size="12" fill="white" text-anchor="middle" dominant-baseline="middle">$text</text>
</svg>
EOF
}

# Food lifestyle placeholders
create_placeholder "public/assets/images/food_lifestyle/lentils.jpeg" "Lentils"
create_placeholder "public/assets/images/food_lifestyle/brocolli.jpeg" "Broccoli"
create_placeholder "public/assets/images/food_lifestyle/garlic.jpeg" "Garlic"
create_placeholder "public/assets/images/food_lifestyle/onions.jpeg" "Onions"
create_placeholder "public/assets/images/food_lifestyle/jersulam.jpeg" "Jerusalem"
create_placeholder "public/assets/images/food_lifestyle/walking.jpeg" "Walking"
create_placeholder "public/assets/images/food_lifestyle/cycling.jpeg" "Cycling"
create_placeholder "public/assets/images/food_lifestyle/swimming.png" "Swimming"
create_placeholder "public/assets/images/food_lifestyle/yoga.png" "Yoga"
create_placeholder "public/assets/images/food_lifestyle/meditation.png" "Meditation"
create_placeholder "public/assets/images/food_lifestyle/deepBreathing.jpeg" "Breathing"

# Probiotic images placeholders
create_placeholder "public/assets/images/probiotics_images/Bifidobacterium Probiotic Complex.jpeg" "Bifido"
create_placeholder "public/assets/images/probiotics_images/Lactobacillus Probiotic.jpeg" "Lacto"
create_placeholder "public/assets/images/probiotics_images/Akkermansia Probiotic Blend.jpeg" "Akkermansia"
create_placeholder "public/assets/images/probiotics_images/Bacillus Probiotic.jpeg" "Bacillus"
create_placeholder "public/assets/images/probiotics_images/Premium Inulin Fiber Supplement.jpeg" "Inulin"
create_placeholder "public/assets/images/probiotics_images/High-Potency Fish Oil Complex.jpeg" "Fish Oil"
create_placeholder "public/assets/images/probiotics_images/Vitamin D Complex.jpeg" "Vitamin D"
create_placeholder "public/assets/images/probiotics_images/Zinc Complex.jpeg" "Zinc"

echo -e "${GREEN}✅ Placeholder images created${NC}"

echo -e "${YELLOW}🔨 Step 4: Rebuilding frontend with correct API URL...${NC}"
export REACT_APP_API_BASE_URL="$BACKEND_URL"
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend built successfully${NC}"
else
    echo -e "${RED}❌ Frontend build failed${NC}"
    exit 1
fi

echo -e "${YELLOW}📤 Step 5: Deploying to S3...${NC}"
aws s3 sync build/ "s3://$S3_BUCKET" --delete --region us-east-2

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Files uploaded to S3${NC}"
else
    echo -e "${RED}❌ S3 upload failed${NC}"
    exit 1
fi

echo -e "${YELLOW}🔄 Step 6: Invalidating CloudFront cache...${NC}"
aws cloudfront create-invalidation \
    --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
    --paths "/*" \
    --region us-east-2

echo ""
echo -e "${GREEN}🎉 All fixes applied!${NC}"
echo ""
echo -e "${YELLOW}📋 What was fixed:${NC}"
echo "1. ✅ API URL updated to: $BACKEND_URL"
echo "2. ✅ Placeholder images created for all missing assets"
echo "3. ✅ Frontend rebuilt with correct configuration"
echo "4. ✅ Files deployed to S3"
echo "5. ✅ CloudFront cache invalidated"
echo ""
echo -e "${YELLOW}🧪 Test your application:${NC}"
echo "Frontend: https://dfjabnv013m4m.cloudfront.net"
echo "Wait 5-10 minutes for CloudFront invalidation to complete"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Replace placeholder images with real images in public/assets/images/"
echo "2. Ensure your backend has all required API endpoints"
echo "3. Test all functionality"
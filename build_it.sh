#!/usr/bin/env bash
set -e

# Usage: ./build_it.sh <arch/machine> [base_image]
# Examples:
#   ./build_it.sh amd64
#   ./build_it.sh rpi4
#   ./build_it.sh aarch64 ghcr.io/siksil/aarch64-inpui-base:2026.01.0

INPUT_ARCH=$1
USER_BASE_IMAGE=$2

if [ -z "$INPUT_ARCH" ]; then
    echo "Usage: $0 <arch/machine> [base_image]"
    echo "Examples: amd64, aarch64, rpi3, rpi4, rpi5"
    exit 1
fi

# Map Architecture
case $INPUT_ARCH in
    rpi3|rpi4|rpi5|aarch64)
        ARCH="aarch64"
        ;;
    amd64|x86_64)
        ARCH="amd64"
        ;;
    *)
        ARCH=$INPUT_ARCH
        ;;
esac

# Set Base Image
if [ -z "$USER_BASE_IMAGE" ]; then
    BASE_IMAGE="ghcr.io/home-assistant/${ARCH}-base:latest"
else
    BASE_IMAGE=$USER_BASE_IMAGE
fi

echo "--- Configuration ---"
echo "Target Arch:  $ARCH (from $INPUT_ARCH)"
echo "Base Image:   $BASE_IMAGE"

# 1. Detect Core Version from pyproject.toml
CORE_VERSION=$(grep -E '^version = ' pyproject.toml | cut -d '"' -f 2)
if [ -z "$CORE_VERSION" ]; then
    echo "Error: Could not detect version from pyproject.toml"
    exit 1
fi
echo "Core Version: $CORE_VERSION"

# 2. Find and Validate Frontend Wheel
FRONTEND_WHEEL=$(ls home_assistant_frontend-*.whl 2>/dev/null | head -n 1)
if [ -z "$FRONTEND_WHEEL" ]; then
    echo "Error: No home_assistant_frontend-*.whl found in the root directory."
    echo "Please place your locally compiled frontend wheel here first."
    exit 1
fi

# Extract Frontend Version from wheel filename
# Format: home_assistant_frontend-20260325.8-py3-none-any.whl
FRONTEND_VERSION=$(echo "$FRONTEND_WHEEL" | sed -E 's/home_assistant_frontend-(.*)-py3-none-any.whl/\1/')
echo "Frontend Whl: $FRONTEND_WHEEL (Version: $FRONTEND_VERSION)"

# 3. Patch manifest.json and package_constraints.txt
echo "Patching version pins..."
# Update manifest.json
sed -i "s/\"home-assistant-frontend==.*\"/\"home-assistant-frontend==$FRONTEND_VERSION\"/" inpui/components/frontend/manifest.json
# Update package_constraints.txt
sed -i "s/home-assistant-frontend==.*/home-assistant-frontend==$FRONTEND_VERSION/" inpui/package_constraints.txt

# 4. Build the Docker Image
FINAL_TAG="ghcr.io/siksil/${INPUT_ARCH}_inpui_core:${CORE_VERSION}"
echo "Building Image: $FINAL_TAG"

docker build \
    --build-arg BUILD_FROM="$BASE_IMAGE" \
    -t "$FINAL_TAG" .

echo ""
echo "--- Success! ---"
echo "Image built and tagged as: $FINAL_TAG"
echo "You can now manually push it using: docker push $FINAL_TAG"

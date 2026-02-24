#!/bin/bash
set -e

# Default values
DEFAULT_NAME=""
DEFAULT_VERSION=""
USE_GITTAG=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --gittag)
            USE_GITTAG=true
            shift
            ;;
        --name=*)
            DEFAULT_NAME="${1#*=}"
            shift
            ;;
        --version=*)
            DEFAULT_VERSION="${1#*=}"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--gittag] [--name=<name>] [--version=<version>]"
            exit 1
            ;;
    esac
done

# Extract package name with fallback
PACKAGE_NAME=$(uv run --no-project --isolated --with tomli python -c "
import tomli
import sys
with open('pyproject.toml', 'rb') as f:
    data = tomli.load(f)
    name = data.get('project', {}).get('name', '${DEFAULT_NAME}')
    if not name:
        print('ERROR: No package name found in pyproject.toml and no --name provided', file=sys.stderr)
        sys.exit(1)
    print(name)
")

# Extract version with fallback
VERSION=$(uv run --no-project --isolated --with tomli python -c "
import tomli
import sys
with open('pyproject.toml', 'rb') as f:
    data = tomli.load(f)
    version = data.get('project', {}).get('version', '${DEFAULT_VERSION}')
    if not version:
        print('ERROR: No version found in pyproject.toml and no --version provided', file=sys.stderr)
        sys.exit(1)
    print(version)
")

# Build iteration string if --gittag is specified
ITERATION_FLAG=""
if [ "$USE_GITTAG" = true ]; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        GITTAG=$(git log --format=%ct.%h -1 2>/dev/null || echo "0.unknown")
        ITERATION_FLAG="--iteration 1.${GITTAG}"
        echo "Building ${PACKAGE_NAME} ${VERSION}-1.${GITTAG}..."
    else
        echo "Warning: --gittag specified but not in a git repository"
        echo "Building ${PACKAGE_NAME} ${VERSION}..."
    fi
else
    echo "Building ${PACKAGE_NAME} ${VERSION}..."
fi

# Build wheel
uv build --python python3.9

# Create staging directory
STAGING_DIR=$(mktemp -d)
trap "rm -rf ${STAGING_DIR}" EXIT

INSTALL_DIR="${STAGING_DIR}/usr/lib/python3.9/site-packages"
mkdir -p "${INSTALL_DIR}"

# Use uv pip to install the wheel to the staging directory
uv pip install --target "${INSTALL_DIR}" --no-deps dist/*.whl

# Clean up lock files
find "${STAGING_DIR}" -name "*.lock" -delete

# Build RPM dependencies
RPM_DEPS=$(uv run --no-project extract_rpm_deps.py)

# Build RPM from directory
eval "fpm -s dir -t rpm \
    --name 'python3-${PACKAGE_NAME}' \
    --version '${VERSION}' \
    ${ITERATION_FLAG} \
    --architecture x86_64 \
    --depends python3.9 \
    ${RPM_DEPS} \
    --rpm-dist el9 \
    -C ${STAGING_DIR} \
    usr/lib/python3.9/site-packages"

echo "RPM built successfully!"
ls -lh python3-${PACKAGE_NAME}*.rpm


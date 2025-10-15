#!/bin/bash
set -e

echo "Deleting migration files from all Django apps..."

# Find all migration directories and delete numbered migration files
find . -path "*/migrations/00*.py" -delete
find . -path "*/migrations/00*.pyc" -delete

echo "✓ Migration files deleted"
echo ""
echo "Keeping __init__.py files intact"
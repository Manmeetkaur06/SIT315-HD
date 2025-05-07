#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
g++ "$DIR/image_enhance_openmp.cpp" -fopenmp -o "$DIR/enhance" $(pkg-config --cflags --libs opencv4)

echo "✅  Built $DIR/enhance"

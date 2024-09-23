#!/bin/bash

# 设置镜像名称和保存的文件名
IMAGE_NAME="server-monitor-frontend"
OUTPUT_FILE="server-monitor-frontend.tar"

# 构建 Docker 镜像
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# 输出构建结果的退出码
BUILD_EXIT_CODE=$?
echo "Build Exit Code: $BUILD_EXIT_CODE"

# 检查构建是否成功
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "Docker image built successfully."

    # 保存镜像为 .tar 文件
    echo "Saving Docker image to $OUTPUT_FILE..."
    docker save -o $OUTPUT_FILE $IMAGE_NAME

    # 检查镜像保存是否成功
    SAVE_EXIT_CODE=$?
    if [ $SAVE_EXIT_CODE -eq 0 ]; then
        echo "Docker image saved successfully to $OUTPUT_FILE."
    else
        echo "Failed to save Docker image."
        exit 1
    fi
else
    echo "Docker image build failed."
    exit 1
fi

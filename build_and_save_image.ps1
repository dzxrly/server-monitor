# 定义镜像名称和保存的文件名
$ImageName = "server-monitor-frontend"
$OutputFile = "server-monitor-frontend.tar"

# 构建 Docker 镜像
Write-Host "Building Docker image..."
docker build -t $ImageName .

# 输出构建结果的退出码
$buildExitCode = $LASTEXITCODE
Write-Host "Build Exit Code: $buildExitCode"

# 检查构建是否成功
if ($buildExitCode -eq 0)
{
    Write-Host "Docker image built successfully."

    # 保存镜像为 .tar 文件
    Write-Host "Saving Docker image to $OutputFile..."
    docker save -o $OutputFile $ImageName

    # 检查镜像保存是否成功
    $saveExitCode = $LASTEXITCODE
    if ($saveExitCode -eq 0)
    {
        Write-Host "Docker image saved successfully to $OutputFile."
    }
    else
    {
        Write-Host "Failed to save Docker image."
        exit 1
    }
}
else
{
    Write-Host "Docker image build failed."
    exit 1
}

# GS3D文档网站部署脚本 (deploy.ps1)
param (
    [string]$RepoUrl = "https://github.com/MEKXH/gs3d.git",
    [string]$BranchName = "gh-pages",
    [switch]$Force = $false
)

# 显示标题
function Show-Header {
    param ([string]$Title)
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
}

# 显示步骤
function Show-Step {
    param ([string]$Message)
    Write-Host "`n>> $Message" -ForegroundColor Green
}

# 显示信息
function Show-Info {
    param ([string]$Message)
    Write-Host $Message -ForegroundColor Gray
}

# 显示成功
function Show-Success {
    param ([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

# 显示错误
function Show-Error {
    param ([string]$Message)
    Write-Host "`n[Error] $Message" -ForegroundColor Red
}

# 检查命令是否存在
function Test-CommandExists {
    param ([string]$Command)
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# 检查要求
function Test-Requirements {
    Show-Step "Checking deployment requirements..."

    # 检查Git
    if (-not (Test-CommandExists "git")) {
        Show-Error "Git is not installed. Please install Git: https://git-scm.com/downloads"
        return $false
    }
    Show-Info "✅ Git is installed"

    # 检查pnpm
    if (-not (Test-CommandExists "pnpm")) {
        Show-Error "pnpm is not installed. Please install pnpm: npm install -g pnpm"
        return $false
    }
    Show-Info "✅ pnpm is installed"

    # 检查Node.js
    if (-not (Test-CommandExists "node")) {
        Show-Error "Node.js is not installed. Please install Node.js: https://nodejs.org/"
        return $false
    }
    $nodeVersion = (node -v)
    if ([version]::Parse($nodeVersion.Substring(1)) -lt [version]::Parse("18.0.0")) {
        Show-Error "Node.js version is too low. VitePress requires Node.js 18.0.0 or higher"
        return $false
    }
    Show-Info "✅ Node.js is installed (Version: $nodeVersion)"

    return $true
}

# 清理缓存
function Clear-ViteCache {
    Show-Step "Clearing VitePress cache..."

    # 清理VitePress缓存
    Remove-Item -Recurse -Force "docs/.vitepress/.temp" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "docs/.vitepress/.cache" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "node_modules/.vite" -ErrorAction SilentlyContinue

    # 清理dist文件夹
    if (Test-Path "docs/.vitepress/dist") {
        Remove-Item -Recurse -Force "docs/.vitepress/dist"
    }

    Show-Info "✅ Cache cleared"
}

# 安装依赖
function Install-Dependencies {
    Show-Step "Installing project dependencies..."

    # 检查package.json是否存在
    if (-not (Test-Path "package.json")) {
        Show-Error "package.json file not found. Make sure you are in the right project directory."
        return $false
    }

    # 安装依赖
    try {
        pnpm install
        Show-Info "✅ Dependencies installed successfully"
        return $true
    }
    catch {
        Show-Error "Failed to install dependencies: $_"
        return $false
    }
}

# 构建网站
function Invoke-WebsiteBuild {
    Show-Step "Building documentation website..."

    try {
        pnpm docs:build

        if (-not (Test-Path "docs/.vitepress/dist")) {
            Show-Error "Build successful, but dist directory not found"
            return $false
        }

        Show-Info "✅ Website built successfully"
        return $true
    }
    catch {
        Show-Error "Website build failed: $_"
        return $false
    }
}

# 部署到GitHub Pages
function Publish-ToGitHubPages {
    param (
        [string]$RepoUrl,
        [string]$BranchName,
        [bool]$Force
    )

    Show-Step "Deploying to GitHub Pages ($BranchName branch)..."

    # 切换到dist目录
    Set-Location "docs/.vitepress/dist"

    # 初始化git
    git init
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Git initialization failed"
        return $false
    }

    # 添加所有文件
    git add -A
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Git add files failed"
        return $false
    }

    # 提交更改
    git commit -m "deploy: update documentation [$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]"
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Git commit failed"
        return $false
    }

    # 设置远程仓库
    git remote add origin $RepoUrl
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Setting Git remote repository failed"
        return $false
    }

    # 推送到GitHub
    $forceFlag = if ($Force) { "-f" } else { "" }
    $command = "git push $forceFlag origin master:$BranchName"

    Show-Info "Executing: $command"
    Invoke-Expression $command

    if ($LASTEXITCODE -ne 0) {
        Show-Error "Push to GitHub failed"
        return $false
    }

    # 返回到原始目录
    Set-Location -Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
    if (-not $PSScriptRoot) {
        Set-Location -Path (Split-Path -Parent (Split-Path -Parent (Get-Location)))
    }

    Show-Info "✅ Deployment complete"
    return $true
}

# 主函数
function Start-Deployment {
    Show-Header "GS3D Documentation Website Deployment Tool"

    # 检查要求
    if (-not (Test-Requirements)) {
        return
    }

    # 清理缓存
    Clear-ViteCache

    # 安装依赖
    if (-not (Install-Dependencies)) {
        return
    }

    # 构建网站
    if (-not (Invoke-WebsiteBuild)) {
        return
    }

    # 部署到GitHub Pages
    if (Publish-ToGitHubPages -RepoUrl $RepoUrl -BranchName $BranchName -Force $Force) {
        Show-Success "`nCongratulations! GS3D documentation has been successfully deployed to GitHub Pages."
        Show-Success "Please visit https://mekxh.github.io/gs3d/ to view your website."
    }
}

# 执行主函数
Start-Deployment
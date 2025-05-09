# G3SD文档网站部署脚本 (deploy.ps1)
param (
    [string]$RepoUrl = "https://https://github.com/MEKXH/gs3d-doc.git",
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
    Write-Host "`n[错误] $Message" -ForegroundColor Red
}

# 检查命令是否存在
function Test-CommandExists {
    param ([string]$Command)
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# 检查要求
function Test-Requirements {
    Show-Step "检查部署要求..."

    # 检查Git
    if (-not (Test-CommandExists "git")) {
        Show-Error "未安装Git。请先安装Git: https://git-scm.com/downloads"
        return $false
    }
    Show-Info "✅ Git已安装"

    # 检查pnpm
    if (-not (Test-CommandExists "pnpm")) {
        Show-Error "未安装pnpm。请先安装pnpm: npm install -g pnpm"
        return $false
    }
    Show-Info "✅ pnpm已安装"

    # 检查Node.js
    if (-not (Test-CommandExists "node")) {
        Show-Error "未安装Node.js。请先安装Node.js: https://nodejs.org/"
        return $false
    }
    $nodeVersion = (node -v)
    if ([version]::Parse($nodeVersion.Substring(1)) -lt [version]::Parse("18.0.0")) {
        Show-Error "Node.js版本太低。VitePress需要Node.js 18.0.0或更高版本"
        return $false
    }
    Show-Info "✅ Node.js已安装 (版本: $nodeVersion)"

    return $true
}

# 清理缓存
function Clear-ViteCache {
    Show-Step "清理VitePress缓存..."

    # 清理VitePress缓存
    Remove-Item -Recurse -Force "docs/.vitepress/.temp" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "docs/.vitepress/.cache" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "node_modules/.vite" -ErrorAction SilentlyContinue

    # 清理dist文件夹
    if (Test-Path "docs/.vitepress/dist") {
        Remove-Item -Recurse -Force "docs/.vitepress/dist"
    }

    Show-Info "✅ 缓存已清理"
}

# 安装依赖
function Install-Dependencies {
    Show-Step "安装项目依赖..."

    # 检查package.json是否存在
    if (-not (Test-Path "package.json")) {
        Show-Error "未找到package.json文件。请确保你在正确的项目目录中。"
        return $false
    }

    # 安装依赖
    try {
        pnpm install
        Show-Info "✅ 依赖安装成功"
        return $true
    }
    catch {
        Show-Error "依赖安装失败: $_"
        return $false
    }
}

# 构建网站 (使用合规的动词)
function Invoke-WebsiteBuild {
    Show-Step "构建文档网站..."

    try {
        pnpm docs:build

        if (-not (Test-Path "docs/.vitepress/dist")) {
            Show-Error "构建成功，但未找到dist目录"
            return $false
        }

        Show-Info "✅ 网站构建成功"
        return $true
    }
    catch {
        Show-Error "网站构建失败: $_"
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

    Show-Step "部署到GitHub Pages ($BranchName 分支)..."

    # 切换到dist目录
    Set-Location "docs/.vitepress/dist"

    # 初始化git
    git init
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Git初始化失败"
        return $false
    }

    # 添加所有文件
    git add -A
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Git添加文件失败"
        return $false
    }

    # 提交更改
    git commit -m "deploy: update documentation [$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]"
    if ($LASTEXITCODE -ne 0) {
        Show-Error "Git提交失败"
        return $false
    }

    # 设置远程仓库
    git remote add origin $RepoUrl
    if ($LASTEXITCODE -ne 0) {
        Show-Error "设置Git远程仓库失败"
        return $false
    }

    # 推送到GitHub
    $forceFlag = if ($Force) { "-f" } else { "" }
    $command = "git push $forceFlag origin master:$BranchName"

    Show-Info "执行: $command"
    Invoke-Expression $command

    if ($LASTEXITCODE -ne 0) {
        Show-Error "推送到GitHub失败"
        return $false
    }

    # 返回到原始目录
    Set-Location -Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
    if (-not $PSScriptRoot) {
        Set-Location -Path (Split-Path -Parent (Split-Path -Parent (Get-Location)))
    }

    Show-Info "✅ 部署完成"
    return $true
}

# 主函数
function Start-Deployment {
    Show-Header "G3SD文档网站部署工具"

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
        Show-Success "`n恭喜！G3SD文档已成功部署到GitHub Pages。"
        Show-Success "请访问 https://yourusername.github.io/G3SD/ 查看你的网站。"
    }
}

# 执行主函数
Start-Deployment
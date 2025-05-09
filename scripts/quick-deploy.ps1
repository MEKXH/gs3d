# GS3D文档快速部署脚本
# 使用方法: .\quick-deploy.ps1 -RepoUrl "https://github.com/MEKXH/gs3d.git"

param (
    [Parameter(Mandatory = $false)]  # 设为非必需，使用默认值
    [string]$RepoUrl = "https://github.com/MEKXH/gs3d.git", # 提供默认值
    [string]$BranchName = "gh-pages",
    [switch]$Force = $false
)

Write-Host "开始部署GS3D文档网站..." -ForegroundColor Cyan

# 检查Git是否安装
if (-not (Get-Command -Name "git" -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未安装Git。请先安装Git: https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# 检查pnpm是否安装
if (-not (Get-Command -Name "pnpm" -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未安装pnpm。请先安装pnpm: npm install -g pnpm" -ForegroundColor Red
    exit 1
}

# 清理缓存和构建目录
Write-Host "清理缓存..." -ForegroundColor Yellow
Remove-Item -Recurse -Force "docs/.vitepress/.temp" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "docs/.vitepress/.cache" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "docs/.vitepress/dist" -ErrorAction SilentlyContinue

# 安装依赖
Write-Host "安装依赖..." -ForegroundColor Yellow
pnpm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 依赖安装失败" -ForegroundColor Red
    exit 1
}

# 构建文档
Write-Host "构建文档网站..." -ForegroundColor Yellow
pnpm docs:build
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 文档构建失败" -ForegroundColor Red
    exit 1
}

# 部署到GitHub Pages
Write-Host "部署到GitHub Pages..." -ForegroundColor Yellow
Set-Location "docs/.vitepress/dist"

# 初始化Git仓库并提交文件
git init
git add -A
git commit -m "deploy: update documentation $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 推送到GitHub
$forceFlag = if ($Force) { "-f" } else { "" }
git push $forceFlag "${RepoUrl}" master:$BranchName

# 返回原目录
Set-Location -Path (Split-Path -Parent (Split-Path -Parent (Get-Location)))

if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 部署失败" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ 部署成功!" -ForegroundColor Green
Write-Host "请访问 https://mekxh.github.io/gs3d/ 查看你的文档网站" -ForegroundColor Green
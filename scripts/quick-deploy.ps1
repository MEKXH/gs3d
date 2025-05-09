# GS3D Documentation Quick Deployment Script
# Usage: .\quick-deploy.ps1 [-Force]

param (
    [string]$RepoUrl = "https://github.com/MEKXH/gs3d.git",
    [string]$BranchName = "gh-pages",
    [switch]$Force = $false
)

Write-Host "Starting GS3D documentation deployment..." -ForegroundColor Cyan

# Check if Git is installed
if (-not (Get-Command -Name "git" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed. Please install Git: https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# Check if pnpm is installed
if (-not (Get-Command -Name "pnpm" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pnpm is not installed. Please install pnpm: npm install -g pnpm" -ForegroundColor Red
    exit 1
}

# Clean cache and build directory
Write-Host "Cleaning cache..." -ForegroundColor Yellow
Remove-Item -Recurse -Force "docs/.vitepress/.temp" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "docs/.vitepress/.cache" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "docs/.vitepress/dist" -ErrorAction SilentlyContinue

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pnpm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Build documentation
Write-Host "Building documentation website..." -ForegroundColor Yellow
pnpm docs:build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Documentation build failed" -ForegroundColor Red
    exit 1
}

# Deploy to GitHub Pages
Write-Host "Deploying to GitHub Pages..." -ForegroundColor Yellow
Set-Location "docs/.vitepress/dist"

# Initialize Git repository and commit files
git init
git add -A
git commit -m "deploy: update documentation $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# Push to GitHub
$forceFlag = if ($Force) { "-f" } else { "" }
git push $forceFlag "${RepoUrl}" master:$BranchName

# Return to original directory
Set-Location -Path (Split-Path -Parent (Split-Path -Parent (Get-Location)))

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Deployment successful!" -ForegroundColor Green
Write-Host "Please visit https://mekxh.github.io/gs3d/ to view your documentation website" -ForegroundColor Green
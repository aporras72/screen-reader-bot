# Screen Reader Bot Installer for Windows
# Run this in PowerShell as Administrator

Write-Host "🤖 Screen Reader Bot Installer" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "✗ Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Check Python
Write-Host "`n📋 Checking Python installation..." -ForegroundColor Yellow
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if ($pythonPath) {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
}
else {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Install Python dependencies
Write-Host "`n📋 Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check Chocolatey
Write-Host "`n📋 Checking Chocolatey..." -ForegroundColor Yellow
$chocoPath = Get-Command choco -ErrorAction SilentlyContinue
if ($chocoPath) {
    Write-Host "✓ Chocolatey found" -ForegroundColor Green
}
else {
    Write-Host "📦 Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    $env:Path += ";C:\ProgramData\chocolatey\bin"
    Write-Host "✓ Chocolatey installed" -ForegroundColor Green
}

# Install Tesseract
Write-Host "`n📋 Installing Tesseract OCR..." -ForegroundColor Yellow
$tesseractPath = Get-Command tesseract -ErrorAction SilentlyContinue
if ($tesseractPath) {
    Write-Host "✓ Tesseract already installed" -ForegroundColor Green
}
else {
    Write-Host "Installing Tesseract..." -ForegroundColor Yellow
    choco install tesseract -y
    $env:Path += ";C:\Program Files\Tesseract-OCR"
    Write-Host "✓ Tesseract installed" -ForegroundColor Green
}

Write-Host "`n✅ Installation complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Make sure Claude is running on http://127.0.0.1:8082" -ForegroundColor White
Write-Host "2. Run the bot: python screen_reader.py" -ForegroundColor White
Write-Host "3. The bot will monitor your screen every 10 seconds" -ForegroundColor White
Write-Host "4. Press Ctrl+C to stop" -ForegroundColor White
Write-Host "`n🚀 Ready to go!" -ForegroundColor Green

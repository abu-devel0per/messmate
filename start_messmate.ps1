# ============================================================
#  MessMate - Permanent Startup Script
#  Starts backend + updates frontend env with correct local IP.
#  Usage:  powershell -ExecutionPolicy Bypass -File "start_messmate.ps1"
#  Or:     Right-click > "Run with PowerShell"
# ============================================================

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"
$cloudflaredExe = Join-Path $scriptDir "cloudflared.exe"

Write-Host ""
Write-Host "  __  __                __  __       _       " -ForegroundColor Cyan
Write-Host " |  \/  | ___  ___ ___|  \/  | __ _| |_ ___ " -ForegroundColor Cyan
Write-Host " | |\/| |/ _ \/ __/ __| |\/| |/ _\` | __/ _ \" -ForegroundColor Cyan
Write-Host " | |  | |  __/\__ \__ \ |  | | (_| | ||  __/" -ForegroundColor Cyan
Write-Host " |_|  |_|\___||___/___/_|  |_|\__,_|\__\___| " -ForegroundColor Cyan
Write-Host ""
Write-Host " Startup Script v2.0" -ForegroundColor DarkCyan
Write-Host "========================================" -ForegroundColor DarkCyan
Write-Host ""

# -- 1. Kill old processes on port 8000 --
Write-Host "[1/5] Cleaning up stale processes on port 8000..." -ForegroundColor Yellow
$connections = netstat -ano | Select-String "TCP.*:8000\s"
foreach ($line in $connections) {
    $pid = ($line.ToString().Trim() -split "\s+")[-1]
    if ($pid -match "^\d+$" -and $pid -ne "0") {
        Stop-Process -Id ([int]$pid) -Force -ErrorAction SilentlyContinue
    }
}
Start-Sleep -Seconds 1
Write-Host "  Done." -ForegroundColor Green

# -- 2. Check MongoDB --
Write-Host "[2/5] Checking MongoDB (port 27017)..." -ForegroundColor Yellow
$mongo = netstat -ano | Select-String ":27017"
if ($mongo) {
    Write-Host "  MongoDB is running." -ForegroundColor Green
} else {
    Write-Host "  WARNING: MongoDB NOT detected on port 27017!" -ForegroundColor Red
    Write-Host "  Please start MongoDB and re-run this script." -ForegroundColor Red
    Read-Host "Press ENTER to exit"
    exit 1
}

# -- 3. Detect local IP and update frontend env --
Write-Host "[3/5] Detecting local IP and updating frontend config..." -ForegroundColor Yellow
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notmatch "^127\." -and
    $_.IPAddress -notmatch "^169\.254" -and
    $_.InterfaceAlias -notmatch "vEthernet" -and
    $_.InterfaceAlias -notmatch "Docker" -and
    $_.InterfaceAlias -notmatch "WSL"
} | Sort-Object -Property @{Expression={if ($_.InterfaceAlias -match "Wi-Fi|Ethernet") {0} else {1}}} | Select-Object -First 1 -ExpandProperty IPAddress)

if (-not $localIP) {
    $localIP = "127.0.0.1"
    Write-Host "  Could not detect physical LAN IP, using 127.0.0.1" -ForegroundColor Yellow
} else {
    Write-Host "  Detected Active LAN IP: $localIP" -ForegroundColor Green
}

$backendUrl = "http://${localIP}:8000"
Set-Content -Path (Join-Path $frontendDir ".env") -Value "EXPO_PUBLIC_BACKEND_URL=$backendUrl" -Encoding UTF8
Set-Content -Path (Join-Path $frontendDir ".env.local") -Value "EXPO_PUBLIC_BACKEND_URL=$backendUrl" -Encoding UTF8
Write-Host "  Frontend configured to use: $backendUrl" -ForegroundColor Green

# -- 4. Start Backend --
Write-Host "[4/5] Starting Backend server (uvicorn)..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload" `
    -WorkingDirectory $backendDir `
    -WindowStyle Normal `
    -PassThru

Write-Host "  Backend starting... PID: $($backendProcess.Id)" -ForegroundColor Green

# Wait for backend to be ready (poll up to 30s)
$maxWait = 30
$waited = 0
$ready = $false
Write-Host "  Waiting for backend to be ready..." -ForegroundColor Gray
do {
    Start-Sleep -Seconds 2
    $waited += 2
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/api" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch { }
    Write-Host "  Still starting... ($waited/$maxWait s)" -ForegroundColor Gray
} while ($waited -lt $maxWait)

if ($ready) {
    Write-Host "  Backend is READY!" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Backend may not have started correctly. Check the server window." -ForegroundColor Red
}

# -- 5. Optional: Cloudflare Tunnel for remote access --
Write-Host "[5/5] Tunnel (optional public access)..." -ForegroundColor Yellow
$startTunnel = Read-Host "  Start Cloudflare Tunnel for public URL? (y/N)"
if ($startTunnel -match "^[yY]") {
    if (Test-Path $cloudflaredExe) {
        $tunnelProcess = Start-Process -FilePath $cloudflaredExe `
            -ArgumentList "tunnel", "--url", "http://localhost:8000" `
            -WindowStyle Normal `
            -PassThru
        Write-Host "  Tunnel started! Check the Cloudflare window for your public URL." -ForegroundColor Green
        Write-Host "  Copy that URL to frontend/.env as EXPO_PUBLIC_BACKEND_URL" -ForegroundColor Yellow
    } else {
        Write-Host "  cloudflared.exe not found. Skipping tunnel." -ForegroundColor Gray
    }
} else {
    Write-Host "  Skipping tunnel. Using local IP: $backendUrl" -ForegroundColor Gray
}

# -- Done! --
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  MessMate Backend is RUNNING!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  API (local):    http://localhost:8000/api" -ForegroundColor Cyan
Write-Host "  API (LAN):      $backendUrl/api" -ForegroundColor Cyan
Write-Host "  Swagger Docs:   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Frontend .env:  EXPO_PUBLIC_BACKEND_URL=$backendUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Keep this window open. Press ENTER to close (servers continue running)." -ForegroundColor Gray
Read-Host ""

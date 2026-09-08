# Andiny Atlas Deployment Validation Script
#
# This script validates deployment readiness without modifying
# the backend/.env file.

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendPath = Join-Path $ProjectRoot "backend"

$PythonExecutable = (Get-Command python).Source

$HostAddress = "127.0.0.1"
$Port = 8010

$BaseUrl = "http://${HostAddress}:${Port}"

$ServerProcess = $null


function Write-ValidationHeader {
    param (
        [string]$Message
    )

    Write-Host ""
    Write-Host "=================================================="
    Write-Host $Message
    Write-Host "=================================================="
}


function Stop-ValidationServer {
    if ($null -ne $ServerProcess) {
        if (-not $ServerProcess.HasExited) {
            Write-Host ""
            Write-Host "Stopping validation server..."

            Stop-Process -Id $ServerProcess.Id -Force
        }
    }
}


try {

    Write-ValidationHeader "ANDINY ATLAS DEPLOYMENT VALIDATION"


    # ==================================================
    # 1. Configuration Validation
    # ==================================================

    Write-ValidationHeader "1. CONFIGURATION VALIDATION"

    Push-Location $ProjectRoot

    python -c "
from backend.app.core.settings import Settings

settings = Settings()

print(f'Application: {settings.app_name}')
print(f'Version: {settings.app_version}')
print(f'ENVIRONMENT: {settings.environment}')
print(f'ATLAS_ENV: {settings.atlas_environment}')
print(f'Database: {settings.sqlite_database_name}')
"

    if ($LASTEXITCODE -ne 0) {
        throw "Configuration validation failed."
    }

    Write-Host ""
    Write-Host "Configuration validation PASSED."


    # ==================================================
    # 2. Production Safety Rules
    # ==================================================

    Write-ValidationHeader "2. PRODUCTION SAFETY VALIDATION"

    $SecureJwtSecret = "AndinyAtlasProductionValidationSecret2026!"

    $OriginalEnvironment = $env:ENVIRONMENT
    $OriginalAtlasEnvironment = $env:ATLAS_ENV
    $OriginalDevelopmentSeed = $env:ALLOW_DEVELOPMENT_SEED
    $OriginalJwtSecret = $env:JWT_SECRET_KEY


    Write-Host "Checking production configuration..."

    $env:ENVIRONMENT = "production"
    $env:ATLAS_ENV = "development"
    $env:ALLOW_DEVELOPMENT_SEED = "false"
    $env:JWT_SECRET_KEY = $SecureJwtSecret

    python -c "
from backend.app.core.settings import Settings

settings = Settings()

assert settings.is_production

print('Valid production configuration accepted.')
"

    if ($LASTEXITCODE -ne 0) {
        throw "Valid production configuration was rejected."
    }


    Write-Host ""
    Write-Host "Checking production demo restriction..."

    $env:ATLAS_ENV = "demo"

    python -c "
from backend.app.core.settings import Settings
Settings()
"

    if ($LASTEXITCODE -eq 0) {
        throw "Production incorrectly accepted ATLAS_ENV=demo."
    }

    Write-Host "Production demo restriction PASSED."


    Write-Host ""
    Write-Host "Checking production development seed restriction..."

    $env:ATLAS_ENV = "development"
    $env:ALLOW_DEVELOPMENT_SEED = "true"

    python -c "
from backend.app.core.settings import Settings
Settings()
"

    if ($LASTEXITCODE -eq 0) {
        throw "Production incorrectly accepted development seed behavior."
    }

    Write-Host "Production development seed restriction PASSED."


    Write-Host ""
    Write-Host "Checking production JWT strength requirement..."

    $env:ALLOW_DEVELOPMENT_SEED = "false"
    $env:JWT_SECRET_KEY = "weak-secret"

    python -c "
from backend.app.core.settings import Settings
Settings()
"

    if ($LASTEXITCODE -eq 0) {
        throw "Production incorrectly accepted a weak JWT secret."
    }

    Write-Host "Production JWT strength requirement PASSED."


    # Restore valid production configuration
    $env:JWT_SECRET_KEY = $SecureJwtSecret


    Write-Host ""
    Write-Host "Production safety validation PASSED."


    # ==================================================
    # 3. Application Startup
    # ==================================================

    Write-ValidationHeader "3. APPLICATION STARTUP VALIDATION"

    Write-Host "Starting Andiny Atlas validation server..."

    $ServerProcess = Start-Process `
        -FilePath $PythonExecutable `
        -ArgumentList @(
            "-m",
            "uvicorn",
            "backend.app.main:app",
            "--host",
            $HostAddress,
            "--port",
            $Port
        ) `
        -WorkingDirectory $ProjectRoot `
        -PassThru `
        -NoNewWindow


    # ==================================================
    # Wait for Application Startup
    # ==================================================

    $MaximumAttempts = 20
    $ApplicationStarted = $false

    for ($Attempt = 1; $Attempt -le $MaximumAttempts; $Attempt++) {

        Start-Sleep -Seconds 1

        try {

            $HealthResponse = Invoke-RestMethod `
                -Uri "$BaseUrl/health" `
                -TimeoutSec 2

            if ($HealthResponse.status -eq "running") {
                $ApplicationStarted = $true
                break
            }

        }
        catch {
            # Application may still be starting.
        }
    }


    if (-not $ApplicationStarted) {
        throw "Application failed to start within the validation timeout."
    }

    Write-Host "Application startup PASSED."


    # ==================================================
    # 4. Health Endpoint Validation
    # ==================================================

    Write-ValidationHeader "4. HEALTH ENDPOINT VALIDATION"

    Write-Host "Checking /health..."

    $HealthResponse = Invoke-RestMethod `
        -Uri "$BaseUrl/health"

    if ($HealthResponse.status -ne "running") {
        throw "/health did not return running status."
    }

    Write-Host "/health PASSED."


    Write-Host ""
    Write-Host "Checking /health/live..."

    $LiveResponse = Invoke-RestMethod `
        -Uri "$BaseUrl/health/live"

    if ($LiveResponse.status -ne "alive") {
        throw "/health/live did not return alive status."
    }

    Write-Host "/health/live PASSED."


    # ==================================================
    # 5. Database Readiness Validation
    # ==================================================

    Write-ValidationHeader "5. DATABASE READINESS VALIDATION"

    Write-Host "Checking /health/ready..."

    $ReadyResponse = Invoke-RestMethod `
        -Uri "$BaseUrl/health/ready"

    if ($ReadyResponse.status -ne "ready") {
        throw "/health/ready did not return ready status."
    }

    if ($ReadyResponse.database -ne "available") {
        throw "Database readiness check did not report available."
    }

    Write-Host "/health/ready PASSED."


    # ==================================================
    # Validation Complete
    # ==================================================

    Write-ValidationHeader "DEPLOYMENT VALIDATION SUCCESSFUL"

    Write-Host "All deployment readiness checks passed."
    Write-Host ""
    Write-Host "Validated:"
    Write-Host "  [PASS] Configuration loading"
    Write-Host "  [PASS] Production safety rules"
    Write-Host "  [PASS] Application startup"
    Write-Host "  [PASS] Health endpoint"
    Write-Host "  [PASS] Liveness endpoint"
    Write-Host "  [PASS] Database readiness"


}
finally {

    Stop-ValidationServer

    # Restore original environment variables

    $env:ENVIRONMENT = $OriginalEnvironment
    $env:ATLAS_ENV = $OriginalAtlasEnvironment
    $env:ALLOW_DEVELOPMENT_SEED = $OriginalDevelopmentSeed
    $env:JWT_SECRET_KEY = $OriginalJwtSecret

    Pop-Location
}
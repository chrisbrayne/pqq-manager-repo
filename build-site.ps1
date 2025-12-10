# build-site.ps1
# This script prepares and builds the MkDocs static site by calling the Python build script.
# It serves as a simple wrapper for local use.

[CmdletBinding()]
param (
    [Switch]$DeployToGitHub # Renamed for clarity vs. Netlify
)

# --- Configuration ---
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PythonBuildScript = Join-Path $PSScriptRoot "build_menu.py"

# --- Main Logic ---

# 1. Run the Python script to prepare the site content and navigation
Write-Host "--- Running Python Build Preparation Script ---"
python.exe $PythonBuildScript
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python build preparation script failed."
    exit
}
Write-Host "-------------------------------------------"

# 2. Build the MkDocs site
Write-Host "Running 'mkdocs build'..."
mkdocs build
if ($LASTEXITCODE -ne 0) {
    Write-Error "MkDocs build failed."
    exit
}
Write-Host "MkDocs site built successfully in the 'site' directory."

# 3. Deploy to GitHub Pages if requested
if ($DeployToGitHub.IsPresent) {
    Write-Host "Deploying to GitHub Pages..."
    mkdocs gh-deploy
    if ($LASTEXITCODE -ne 0) {
        Write-Error "MkDocs deployment to GitHub Pages failed."
        exit
    }
    Write-Host "Deployment to GitHub Pages successful."
}

# deploy-to-github.ps1
# This script is an "end-of-day" task to stage all changes, commit them locally,
# and then push them to the remote GitHub repository.

[CmdletBinding()]
param (
    [string]$CommitMessage = "Batch update for local changes"
)

$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$GitRepoDir = $PSScriptRoot

Write-Host "--- Starting Deployment to GitHub ---"

# 1. Stage all changes
Write-Host "  [Git] Staging all changes..."
git -C $GitRepoDir add .
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git add failed. Aborting deployment."
    exit 1
}

# 2. Commit changes
Write-Host "  [Git] Committing with message: '$CommitMessage'"
git -C $GitRepoDir commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Warning "No new changes to commit, or Git commit failed. Proceeding with push."
    # Even if no changes to commit, we might still want to push if there are unpushed commits
}

# 3. Push to remote
Write-Host "  [Git] Pushing changes to remote..."
git -C $GitRepoDir push
if ($LASTEXITCODE -ne 0) {
    Write-Error "Git push failed. Please check your connection or credentials."
    exit 1
}

Write-Host "--- Deployment to GitHub successful ---"

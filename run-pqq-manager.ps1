# PQQ Manager Automation Script - Supports PDF and DOCX in Batch
#
# This script finds all supported documents in the 'incoming' folder, processes them one by one,
# generates a draft response using the Gemini API, commits the result to Git, and moves
# the processed source file to a 'processed' sub-folder.

# --- Configuration ---
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$IncomingDir = Join-Path $PSScriptRoot "incoming"
$ProcessedDir = Join-Path $IncomingDir "processed"
$EvidenceDir = Join-Path $PSScriptRoot "evidence"
$DraftsDir = Join-Path $PSScriptRoot "drafts"
$PythonScript = Join-Path $PSScriptRoot "gemini_processor.py"
$GitRepoDir = $PSScriptRoot # The Git repository root is the same as the script root (pqq-manager)

# --- Main Logic ---

# 1. Create a 'processed' directory if it doesn't exist
if (-not (Test-Path $ProcessedDir)) {
    New-Item -Path $ProcessedDir -ItemType Directory | Out-Null
}

# 2. Find all unprocessed documents in the 'incoming' directory
$supportedExtensions = @("*.pdf", "*.docx")
# The '-File' switch ensures we only get files, not directories.
# The 'Where-Object' ensures we don't try to process files already in the 'processed' sub-folder.
# A wildcard is added to the path to ensure -Include works correctly.
$sourceFiles = Get-ChildItem -Path "$IncomingDir\*" -Include $supportedExtensions -File | Where-Object { $_.DirectoryName -ne $ProcessedDir }

if ($sourceFiles.Count -eq 0) {
    Write-Host "No new PQQ documents (.pdf, .docx) found in the 'incoming' folder."
    exit
}

# Check for API Key before starting
if (-not $env:PQQ_API_KEY) {
    Write-Error "The 'PQQ_API_KEY' environment variable is not set. Please set it before running the script."
    exit
}

# --- AI and File Integration Functions ---
# (These functions remain unchanged)

function Invoke-FileTextExtraction($File) {
    Write-Host "  [PY] Extracting text from $($File.Name)..."
    try {
        $text = python.exe $PythonScript "extract_text" $File.FullName
        return $text
    }
    catch {
        Write-Error "Failed to execute Python script for text extraction. Make sure Python is in your PATH."
        exit
    }
}

function Invoke-GeminiQuestionExtraction($RawText) {
    Write-Host "  [AI] Calling Gemini to extract questions..."
    try {
        $questionsJson = $RawText | python.exe $PythonScript "extract_questions"
        return $questionsJson | ConvertFrom-Json
    }
    catch {
        Write-Error "Failed to parse JSON or execute Python script for question extraction."
        exit
    }
}

function Invoke-GeminiBatchEvidenceSearch($QuestionsList, $EvidencePath) {
    Write-Host "  [AI] Calling Gemini to find evidence for all questions in a single batch..."

    # Recursively find all markdown files in the evidence directory and its subdirectories
    $allEvidence = Get-ChildItem -Path $EvidencePath -Filter "*.md" -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($EvidencePath.Length + 1)
        "--- Evidence File: $relativePath ---`n" + (Get-Content $_.FullName -Raw)
    } | Out-String

    $payload = @{
        questions = $QuestionsList
        evidence  = $allEvidence
    }

    try {
        $resultsJson = $payload | ConvertTo-Json -Depth 5 | python.exe $PythonScript "find_evidence_batch"
        return $resultsJson | ConvertFrom-Json
    }
    catch {
        Write-Error "Failed to parse JSON or execute Python script for batch evidence search."
        exit
    }
}

# --- Git Integration Function ---

function Invoke-GitCommit {
    param(
        [string]$FilePath,
        [string]$CommitMessage
    )
    Write-Host "  [Git] Staging file: $FilePath"
    git -C $GitRepoDir add $FilePath
    if ($LASTEXITCODE -ne 0) { Write-Error "Git add failed." }

    Write-Host "  [Git] Committing with message: '$CommitMessage'"
    git -C $GitRepoDir commit -m $CommitMessage
    if ($LASTEXITCODE -ne 0) { Write-Error "Git commit failed." }

    Write-Host "  [Git] Git commit successful."

    Write-Host "  [Git] Pushing changes to remote..."
    git -C $GitRepoDir push
    if ($LASTEXITCODE -ne 0) { Write-Error "Git push failed." }
    Write-Host "  [Git] Git push successful."
}


# --- Script Execution Loop ---

foreach ($sourceFile in $sourceFiles) {
    Write-Host "--- Processing PQQ: $($sourceFile.Name) ---"

    $rawText = Invoke-FileTextExtraction -File $sourceFile
    if (-not $rawText) {
        Write-Error "Failed to extract text from $($sourceFile.Name). Skipping."
        continue # Move to the next file
    }

    $questions = Invoke-GeminiQuestionExtraction -RawText $rawText
    if ($questions.Count -eq 0) {
        Write-Host "Could not find any questions in $($sourceFile.Name). Skipping."
        # Move the file so we don't re-process it
        Move-Item -Path $sourceFile.FullName -Destination $ProcessedDir
        continue
    }

    Write-Host "Found $($questions.Count) questions. Starting batch evidence search..."
    $answeredQuestions = Invoke-GeminiBatchEvidenceSearch -QuestionsList $questions -EvidencePath $EvidenceDir

    if (-not $answeredQuestions) {
        Write-Error "The batch evidence search returned no results for $($sourceFile.Name). Skipping."
        continue
    }

    Write-Host "Successfully received answers for all questions in $($sourceFile.Name)."

    # Build the draft response
    $draftContent = New-Object System.Text.StringBuilder
    [void]$draftContent.AppendLine("# Draft Response for $($sourceFile.Name)")
    [void]$draftContent.AppendLine("---")
    foreach ($q in $questions) {
        $answer = $answeredQuestions."$q"
        [void]$draftContent.AppendLine("### Q: $q")
        [void]$draftContent.AppendLine()
        [void]$draftContent.AppendLine($answer)
        [void]$draftContent.AppendLine()
        [void]$draftContent.AppendLine("---")
    }

    # Write the final draft to the 'drafts' folder
    $outputFileName = [System.IO.Path]::ChangeExtension($sourceFile.Name, ".md")
    $outputPath = Join-Path $DraftsDir $outputFileName
    Set-Content -Path $outputPath -Value $draftContent.ToString() -Encoding UTF8
    Write-Host "Success! Draft response saved to: $outputPath"

    # Perform Git operations
    $commitMessage = "Auto-filled PQQ draft for $($sourceFile.BaseName)"
    Invoke-GitCommit -FilePath $outputPath -CommitMessage $commitMessage

    # Move the processed file to the 'processed' directory
    Move-Item -Path $sourceFile.FullName -Destination $ProcessedDir
    Write-Host "Moved processed file to '$ProcessedDir'."
    Write-Host "--- Finished Processing: $($sourceFile.Name) ---`n"
}

Write-Host "All files processed."
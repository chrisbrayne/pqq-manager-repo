# PQQ Manager Help Guide

This guide explains how to use the PQQ (Pre-Qualification Questionnaire) Manager system to automatically generate draft responses.

---

## What It Does

This system is designed to speed up the process of filling out PQQs. It works by:
*   Taking PQQ documents (`.pdf` or `.docx` files) from your `incoming/` folder.
*   Using Google's Gemini AI to extract questions and find answers from your **structured library of pre-written "evidence"**.
*   Generating a draft response in Markdown format for each PQQ.
*   Automatically updating a **searchable static website** (using MkDocs) with the new draft and a dynamically generated navigation menu.
*   Bundling all changes into a **local Git commit**, ready for you to review and push to your remote repository for deployment.

---

## How It Works: The Folders

The system is organized into a few key folders:

-   `incoming/`: **Your Starting Point.** Drop new PQQ documents (as `.pdf` or `.docx` files) into this folder.
    *   `incoming/processed/`: After a document is successfully processed, it will be moved here to keep your `incoming/` folder tidy. These files are also listed on the MkDocs site.
-   `evidence/`: **Your Structured Knowledge Base.** This folder contains all the pre-written snippets of information about your company. **Organize these `.md` files into subfolders** (e.g., `evidence/company/`, `evidence/financial/`, `evidence/health_and_safety/`). This structure will be mirrored in the MkDocs website navigation.
-   `drafts/`: **The Output.** After you run the `run-pqq-manager.ps1` script, a new draft response file (e.g., `Client-A-PQQ.md`) will appear here for each processed PQQ. These are automatically added to your Git repository and dynamically linked in the MkDocs site.
    *   `drafts/evidence_library/`: This folder is automatically created and populated by the `build-site.ps1` script to make your evidence visible to MkDocs. You generally don't need to interact with it directly.

---

## Setup Requirements

### Gemini API Key
To use the AI capabilities, you need a Google Gemini API key. This key must be set as a **system-level environment variable** named `PQQ_API_KEY`.

**To set it in PowerShell for the current session (for testing):**
```powershell
$env:PQQ_API_KEY = "YOUR_API_KEY_HERE"
```
For permanent setup, please refer to guides on setting system-level environment variables for Windows.

---

## Step-by-Step Workflow

This workflow is designed for batching changes locally before deploying them in a single push.

### Step 1: Add New PQQ Documents

-   Place one or more new PQQ documents (`.pdf` or `.docx` files) into the `incoming/` folder.

### Step 2: Run the Manager Script

-   Open a PowerShell terminal in the `pqq-manager` folder.
-   Run the main script for each new document:
    ```powershell
    .\run-pqq-manager.ps1
    ```
-   For each document found, the script will:
    *   Generate a Markdown draft in the `drafts/` folder.
    *   **Automatically update the website navigation** to include the new draft.
    *   Create a **local Git commit** containing both the new draft and the updated navigation. It **will not** push to the remote repository.
    *   Move the processed document to `incoming/processed/`.
-   You can repeat Steps 1 and 2 multiple times to create a batch of local changes.

### Step 3: Test Locally (Recommended)

-   After processing all desired files, you can preview the entire site.
-   Run the local web server:
    ```powershell
    mkdocs serve
    ```
-   Open your web browser and go to `http://127.0.0.1:8000`.
-   Verify that all your new drafts appear correctly in the navigation menu and that the content is as expected. Press `Ctrl+C` in the terminal to stop the server when you are done.

### Step 4: Deploy to Netlify

-   When you are satisfied with your batch of local changes, push them to your remote repository.
-   Run the following command from the `pqq-manager` folder:
    ```powershell
    git push
    ```
    Alternatively, you can use the `deploy-to-github.ps1` script for this:
    ```powershell
    .\deploy-to-github.ps1 -CommitMessage "Optional: Your custom commit message"
    ```
-   This will send all your local commits to GitHub, which will automatically trigger Netlify to build and deploy your updated site.

---

## Managing Your Evidence

To maximize the effectiveness of the system:

-   Organize your evidence: **Create subfolders within `evidence/`** (e.g., `evidence/company/`, `evidence/financial/`) and place related `.md` files there. The `build_menu.py` script will automatically create a nested navigation for these on the website.
-   Add New Evidence: Simply create new `.md` files in the appropriate `evidence/` subfolder.
-   Update Existing Evidence: Open an existing `.md` file, make your changes, and save it.

Remember to `git add` and `git commit` any changes to your `evidence/` files manually. You can then push them along with your other batched changes when you are ready to deploy.

---

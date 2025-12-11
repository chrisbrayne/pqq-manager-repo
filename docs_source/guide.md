# PQQ Manager Help Guide

This guide explains how to use the PQQ (Pre-Qualification Questionnaire) Manager system to automatically generate draft responses.

---

## What It Does

This system is designed to speed up the process of filling out PQQs. It works by:
*   Taking PQQ documents (`.pdf` or `.docx` files) from your `incoming/` folder.
*   Using Google's Gemini AI to extract questions from these documents.
*   Searching your **structured library of pre-written "evidence"** (Markdown files in `evidence/` subfolders) for the best answer to each question, also powered by Gemini AI.
*   Generating a draft response in Markdown format for each PQQ, which is saved in the `drafts/` folder.
*   Automatically version controlling these drafts using Git, including committing and pushing to a remote repository (like GitHub).
*   Automatically building a **searchable static website** (using MkDocs) with dynamic navigation from your drafts, evidence library, and a log of processed files, deployed on Netlify.

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

### Step 1: Add New PQQ Documents

-   Place new PQQ documents (as `.pdf` or `.docx` files) into the `incoming/` folder. You can place multiple documents there.

### Step 2: Run the Manager Script

-   Open PowerShell (you can right-click in the `pqq-manager` folder and choose "Open in Terminal").
-   Run the main script with the following command:

    ```powershell
    .\run-pqq-manager.ps1
    ```
-   The script will:
    *   Process **all** supported documents found in `incoming/`.
    *   Extract questions and find matching evidence using Gemini AI.
    *   Generate a Markdown draft in `drafts/` for each document.
    *   Automatically `git add`, `git commit`, and `git push` these new drafts to your remote repository.
    *   Move the processed original document to `incoming/processed/`.

### Step 3: Build and Deploy the Website

After running the manager script and pushing changes to GitHub, you need to rebuild your MkDocs site.

-   Open PowerShell (in the `pqq-manager` folder).
-   **To build and preview locally:**
    ```powershell
    .\build-site.ps1
    mkdocs serve
    ```
    Open your web browser and go to `http://127.0.0.1:8000`. You will see a dynamically generated navigation menu with sections for "PQQ Drafts", "Evidence Library" (structured by folders), and a "Processed Log".
-   **To build and deploy to GitHub Pages (or trigger Netlify deployment):**
    ```powershell
    .\build-site.ps1 -DeployToGitHub
    ```
    *(Note: For Netlify, the `git push` from `run-pqq-manager.ps1` will automatically trigger the build. This local deploy command is primarily for GitHub Pages.)*

### Step 4: Review the Drafts and Website

-   Go to the `drafts/` folder to open and review the generated Markdown files directly.
-   Access your deployed Netlify site (or local `mkdocs serve` preview) to browse your dynamically updated documentation.

---

## Managing Your Evidence

To maximize the effectiveness of the system:

-   Organize your evidence: **Create subfolders within `evidence/`** (e.g., `evidence/company/`, `evidence/financial/`) and place related `.md` files there. The `build-site.ps1` script will automatically create a nested navigation for these on the website.
-   Add New Evidence: Simply create new `.md` files in the appropriate `evidence/` subfolder.
-   Update Existing Evidence: Open an existing `.md` file, make your changes, and save it.

Remember to `git add`, `git commit`, and `git push` any changes to your `evidence/` files manually (or run `run-pqq-manager.ps1` if you've processed a file, which will also commit outstanding changes) to ensure your remote repository and Netlify site are up-to-date.

---

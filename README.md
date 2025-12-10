# PQQ Manager Help Guide

This guide explains how to use the PQQ (Pre-Qualification Questionnaire) Manager system to automatically generate draft responses.

---

## What It Does

This system is designed to speed up the process of filling out PQQs. It works by:
*   Taking PQQ documents (`.pdf` or `.docx` files) from your `incoming/` folder.
*   Using Google's Gemini AI to extract questions from these documents.
*   Searching your library of pre-written "evidence" (Markdown files in `evidence/`) for the best answer to each question, also powered by Gemini AI.
*   Generating a draft response in Markdown format for each PQQ, which is saved in the `drafts/` folder.
*   Automatically version controlling these drafts using Git, including committing and pushing to a remote repository (like GitHub).

---

## How It Works: The Folders

The system is organized into a few key folders:

-   `incoming/`: **Your Starting Point.** Drop new PQQ documents (as `.pdf` or `.docx` files) into this folder.
    *   `incoming/processed/`: After a document is successfully processed, it will be moved here to keep your `incoming/` folder tidy.
-   `evidence/`: **Your Knowledge Base.** This folder contains all the pre-written snippets of information about your company (e.g., insurance details, company history, service descriptions, policies). Each piece of evidence should be a separate `.md` file.
-   `drafts/`: **The Output.** After you run the tool, a new draft response file (e.g., `Client-A-PQQ.md`) will appear here for each processed PQQ. These are automatically added to your Git repository.
-   `docs/`: This folder is intended for use with MkDocs to publish your drafts as a browsable website.

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

### Step 3: Review the Drafts

-   Go to the `drafts/` folder.
-   Open the generated Markdown files (e.g., `Client-A-PQQ.md`) to review, edit, and copy the content as needed. Since they are already committed and pushed, your team can access them via your Git repository.

---

## Managing Your Evidence

You can significantly improve the system's accuracy and coverage by continuously adding to and updating the files in the `evidence/` folder.

-   **To Add New Evidence:** Create a new `.md` file in the `evidence/` folder. Give it a descriptive name (e.g., `sustainability_policy.md`).
-   **To Update Evidence:** Open an existing `.md` file, make your changes, and save it.

The more comprehensive and accurate your evidence library is, the better the automated responses will be. Remember to commit any changes to your `evidence/` files to Git as well.

---

## Viewing the Website (Optional - MkDocs)

To publish your generated drafts and evidence as a browsable static website (e.g., on GitHub Pages):

1.  Open a terminal in the `pqq-manager` folder.
2.  **To preview locally:**
    ```powershell
    mkdocs serve
    ```
    Open your web browser and go to `http://127.0.0.1:8000`.
3.  **To build the static site:**
    ```powershell
    mkdocs build
    ```
4.  **To deploy to GitHub Pages:**
    ```powershell
    mkdocs gh-deploy
    ```
    (Ensure `ghp-import` is installed: `pip install ghp-import`)
# Gemini Context for PQQ Manager

This file serves as a "conversation marker" to bring Gemini up to speed on the project's status, architecture, and workflow. To restore context in a new session, ask Gemini to "load the context file".

---

## Project Overview

The "PQQ Manager" is an automation pipeline to streamline the creation and management of Pre-Qualification Questionnaire (PQQ) responses. It uses Google's Gemini API to process incoming documents and find answers from an evidence library, and MkDocs to generate a searchable static website of the results. The workflow is designed to be local-first, allowing for batching and testing of changes before manual deployment.

---

## Key Files & Scripts

*   `run-pqq-manager.ps1`: The main processing script. It takes a new PQQ document, generates a draft, updates the `mkdocs.yml` navigation menu, and creates a local Git commit.
*   `gemini_processor.py`: The Python script that handles all AI interactions, including text extraction, question identification, and evidence matching.
*   `build_menu.py`: A Python helper script called by the main processor. It dynamically generates the navigation menu for `mkdocs.yml` based on the files in the `drafts/` and `evidence/` directories.
*   `deploy-to-github.ps1`: An "end-of-day" script that stages all local changes, commits them, and pushes them to the remote GitHub repository to trigger a Netlify deployment.
*   `mkdocs.yml`: The configuration file for the MkDocs static site. Its `nav` section is now managed automatically by `build_menu.py`.
*   `guide.md`: The main user guide for the project.
*   `project_log.md`: A log of all significant changes and development activities.

---

## Current Workflow

1.  **Process Files:** The user runs `.\run-pqq-manager.ps1` for each new PQQ document. This creates a draft and a corresponding local commit that includes the automatically updated `mkdocs.yml`.
2.  **Test Locally:** The user runs `mkdocs serve` to preview all batched changes on a local web server.
3.  **Deploy Manually:** When satisfied, the user runs `.\deploy-to-github.ps1` to push all local commits to the remote repository, triggering a Netlify build.

---

## Last Session Summary (2025-12-11)

*   **Automated Navigation:** Implemented a Python script (`build_menu.py`) to automatically generate the navigation menu in `mkdocs.yml`, solving the "manual bottleneck" issue.
*   **Refined Workflow:** Restructured the PowerShell scripts to support a local-first workflow. The main processing script now only creates local commits, and a new `deploy-to-github.ps1` script was created for manual, batched deployments.
*   **Updated Documentation:** The `guide.md` file and `project_log.md` were updated to reflect all the new changes and the current workflow.
*   **Diagnosed API Issue:** Investigated and identified a `429 Quota Exceeded` error from the Gemini API, which was resolved.

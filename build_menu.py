# build_menu.py
# This script prepares the 'docs' directory for MkDocs, consolidating content
# from various sources and dynamically generating the navigation menu.

import os
import shutil
import yaml

# --- Configuration ---
ROOT_DIR = os.path.dirname(__file__)
MKDOCS_CONFIG_FILE = os.path.join(ROOT_DIR, 'mkdocs.yml')

# Source directories for content
DRAFTS_SOURCE_DIR = os.path.join(ROOT_DIR, 'drafts')
EVIDENCE_SOURCE_DIR = os.path.join(ROOT_DIR, 'evidence')
STATIC_DOCS_SOURCE_DIR = os.path.join(ROOT_DIR, 'docs_source') # New static content folder
PROCESSED_LOG_SOURCE_DIR = os.path.join(ROOT_DIR, 'incoming', 'processed') # Source for processed file list

# Destination directory for all MkDocs content (the new docs_dir)
DOCS_BUILD_DIR = os.path.join(ROOT_DIR, 'docs')

# Subdirectories within DOCS_BUILD_DIR for organized content
DRAFTS_DEST_SUBDIR = os.path.join(DOCS_BUILD_DIR, 'pqq_drafts')
EVIDENCE_DEST_SUBDIR = os.path.join(DOCS_BUILD_DIR, 'evidence_library')


def clean_and_create_docs_build_dir():
    """Wipes and recreates the DOCS_BUILD_DIR."""
    print(f"Cleaning and recreating '{DOCS_BUILD_DIR}'...")
    if os.path.exists(DOCS_BUILD_DIR):
        shutil.rmtree(DOCS_BUILD_DIR)
    os.makedirs(DRAFTS_DEST_SUBDIR, exist_ok=True) # Ensure pqq_drafts is created
    os.makedirs(EVIDENCE_DEST_SUBDIR, exist_ok=True) # Ensure evidence_library is created
    print(f"'{DOCS_BUILD_DIR}' is ready.")
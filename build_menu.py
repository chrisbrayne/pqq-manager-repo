# build_menu.py
# This script prepares the 'docs' directory for MkDocs, consolidating content
# from various sources and dynamically generating the navigation menu.

import os
import shutil
import yaml
import time

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
        temp_dir = DOCS_BUILD_DIR + "_temp"
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except PermissionError as e:
                print(f"Warning: Could not delete old temporary directory '{temp_dir}': {e}")
        try:
            os.rename(DOCS_BUILD_DIR, temp_dir)
            shutil.rmtree(temp_dir)
        except (PermissionError, FileExistsError) as e:
            print(f"Warning: Could not delete '{DOCS_BUILD_DIR}': {e}")
    os.makedirs(DRAFTS_DEST_SUBDIR, exist_ok=True)
    print(f"Created '{DRAFTS_DEST_SUBDIR}'")
    os.makedirs(EVIDENCE_DEST_SUBDIR, exist_ok=True)
    print(f"Created '{EVIDENCE_DEST_SUBDIR}'")
    print(f"'{DOCS_BUILD_DIR}' is ready.")

def copy_static_docs():
    """Copies static documentation files to the docs build directory."""
    print(f"Copying files from '{STATIC_DOCS_SOURCE_DIR}' to '{DOCS_BUILD_DIR}'...")
    for item in os.listdir(STATIC_DOCS_SOURCE_DIR):
        source_item = os.path.join(STATIC_DOCS_SOURCE_DIR, item)
        dest_item = os.path.join(DOCS_BUILD_DIR, item)
        if os.path.isfile(source_item):
            shutil.copy2(source_item, dest_item)
            print(f"Copied '{source_item}' to '{dest_item}'")
def copy_content_docs():
    """Copies content from drafts and evidence directories."""
    print("Copying content from 'drafts' and 'evidence' directories...")
    
    # Copying drafts
    for item in os.listdir(DRAFTS_SOURCE_DIR):
        source_item = os.path.join(DRAFTS_SOURCE_DIR, item)
        dest_item = os.path.join(DRAFTS_DEST_SUBDIR, item)
        if os.path.isfile(source_item):
            shutil.copy2(source_item, dest_item)
            print(f"Copied '{source_item}' to '{dest_item}'")

    # Copying evidence
    for root, dirs, files in os.walk(EVIDENCE_SOURCE_DIR):
        for name in files:
            source_item = os.path.join(root, name)
            # Creating a relative path for the destination
            relative_path = os.path.relpath(root, EVIDENCE_SOURCE_DIR)
            dest_dir = os.path.join(EVIDENCE_DEST_SUBDIR, relative_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            dest_item = os.path.join(dest_dir, name)
            shutil.copy2(source_item, dest_item)
            print(f"Copied '{source_item}' to '{dest_item}'")

def main():
    """Main function to build the menu."""
    clean_and_create_docs_build_dir()
    copy_static_docs()
    copy_content_docs()

if __name__ == "__main__":
    main()

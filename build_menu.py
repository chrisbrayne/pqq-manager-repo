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
STATIC_DOCS_SOURCE_DIR = os.path.join(ROOT_DIR, 'docs_source')

# Destination directory for all MkDocs content
DOCS_BUILD_DIR = os.path.join(ROOT_DIR, 'docs')

# Subdirectories within DOCS_BUILD_DIR for organized content
DRAFTS_DEST_SUBDIR_NAME = 'pqq_drafts'
EVIDENCE_DEST_SUBDIR_NAME = 'evidence'
DRAFTS_DEST_SUBDIR = os.path.join(DOCS_BUILD_DIR, DRAFTS_DEST_SUBDIR_NAME)
EVIDENCE_DEST_SUBDIR = os.path.join(DOCS_BUILD_DIR, EVIDENCE_DEST_SUBDIR_NAME)


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
    os.makedirs(EVIDENCE_DEST_SUBDIR, exist_ok=True)
    print(f"'{DOCS_BUILD_DIR}' is ready.")

def copy_static_docs():
    """Copies static documentation files to the docs build directory."""
    print(f"Copying files from '{STATIC_DOCS_SOURCE_DIR}' to '{DOCS_BUILD_DIR}'...")
    for item in os.listdir(STATIC_DOCS_SOURCE_DIR):
        source_item = os.path.join(STATIC_DOCS_SOURCE_DIR, item)
        dest_item = os.path.join(DOCS_BUILD_DIR, item)
        if os.path.isfile(source_item):
            shutil.copy2(source_item, dest_item)

def copy_content_docs():
    """Copies content from drafts and evidence directories."""
    print("Copying content from 'drafts' and 'evidence' directories...")
    # Copying drafts
    if os.path.exists(DRAFTS_SOURCE_DIR):
        for item in os.listdir(DRAFTS_SOURCE_DIR):
            source_item = os.path.join(DRAFTS_SOURCE_DIR, item)
            dest_item = os.path.join(DRAFTS_DEST_SUBDIR, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, dest_item)
    # Copying evidence
    if os.path.exists(EVIDENCE_SOURCE_DIR):
        for root, dirs, files in os.walk(EVIDENCE_SOURCE_DIR):
            for name in files:
                source_item = os.path.join(root, name)
                relative_path = os.path.relpath(root, EVIDENCE_SOURCE_DIR)
                dest_dir = os.path.join(EVIDENCE_DEST_SUBDIR, relative_path)
                os.makedirs(dest_dir, exist_ok=True)
                dest_item = os.path.join(dest_dir, name)
                shutil.copy2(source_item, dest_item)

def generate_and_update_nav():
    """
    Generates the nav structure by scanning directories and updates mkdocs.yml.
    """
    print("Generating dynamic navigation menu...")
    nav = []

    # 1. Add static pages
    nav.append({'Home': 'index.md'})
    nav.append({'Guide': 'guide.md'})

    # 2. Add PQQ Drafts
    if os.path.exists(DRAFTS_DEST_SUBDIR):
        draft_files = sorted([f for f in os.listdir(DRAFTS_DEST_SUBDIR) if f.endswith('.md')])
        if draft_files:
            drafts_nav = []
            for f in draft_files:
                title = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').title()
                path = os.path.join(DRAFTS_DEST_SUBDIR_NAME, f)
                drafts_nav.append({title: path})
            nav.append({'PQQ Drafts': drafts_nav})

    # 3. Add Evidence (hierarchically)
    if os.path.exists(EVIDENCE_DEST_SUBDIR):
        evidence_nav = []
        # Get top-level directories (e.g., 'company', 'financial')
        for category in sorted(os.listdir(EVIDENCE_DEST_SUBDIR)):
            category_path = os.path.join(EVIDENCE_DEST_SUBDIR, category)
            if os.path.isdir(category_path):
                category_title = category.replace('_', ' ').replace('-', ' ').title()
                category_files_nav = []
                # Get files within the category directory
                for f in sorted(os.listdir(category_path)):
                    if f.endswith('.md'):
                        file_title = os.path.splitext(f)[0].replace('_', ' ').replace('-', ' ').title()
                        file_path = os.path.join(EVIDENCE_DEST_SUBDIR_NAME, category, f)
                        category_files_nav.append({file_title: file_path})
                if category_files_nav:
                    evidence_nav.append({category_title: category_files_nav})
        if evidence_nav:
            nav.append({'Evidence': evidence_nav})
    
    # 4. Update mkdocs.yml
    print(f"Updating '{MKDOCS_CONFIG_FILE}' with new navigation...")
    with open(MKDOCS_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    config['nav'] = nav
    
    with open(MKDOCS_CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print("Navigation menu updated successfully.")


def main():
    """Main function to build the menu."""
    clean_and_create_docs_build_dir()
    copy_static_docs()
    copy_content_docs()
    generate_and_update_nav()

if __name__ == "__main__":
    main()

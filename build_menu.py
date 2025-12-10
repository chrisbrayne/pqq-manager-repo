# build_menu.py
# This script prepares all files and dynamically generates the mkdocs.yml navigation menu.

import os
import shutil
import yaml

# --- Configuration ---
ROOT_DIR = os.path.dirname(__file__)
MKDOCS_CONFIG_FILE = os.path.join(ROOT_DIR, 'mkdocs.yml')
DRAFTS_DIR = os.path.join(ROOT_DIR, 'drafts')
EVIDENCE_SOURCE_DIR = os.path.join(ROOT_DIR, 'evidence')
EVIDENCE_DEST_DIR = os.path.join(DRAFTS_DIR, 'evidence_library')
PROCESSED_DIR = os.path.join(ROOT_DIR, 'incoming', 'processed')
PROCESSED_LOG_FILE = os.path.join(DRAFTS_DIR, 'processed_log.md')

def copy_evidence_library():
    """Recursively copies the evidence library into the drafts folder."""
    print("Copying evidence library for MkDocs build...")
    if os.path.exists(EVIDENCE_DEST_DIR):
        shutil.rmtree(EVIDENCE_DEST_DIR)
    shutil.copytree(EVIDENCE_SOURCE_DIR, EVIDENCE_DEST_DIR)

def generate_processed_log():
    """Generates a Markdown file listing all processed PQQ source files."""
    print("Generating a log of processed PQQ files...")
    log_content = ["# Processed Source Documents\n",
                   "This page lists all the source PQQ documents that have been processed by the system.\n"]
    if os.path.exists(PROCESSED_DIR):
        for filename in sorted(os.listdir(PROCESSED_DIR)):
            log_content.append(f"- {filename}\n")
    
    with open(PROCESSED_LOG_FILE, 'w', encoding='utf-8') as f:
        f.writelines(log_content)
    print(f"Created '{PROCESSED_LOG_FILE}'.")

def generate_nav_structure():
    """Builds the nested navigation structure as a Python list of dictionaries."""
    print("Generating new multi-level navigation menu...")
    
    nav = [{'Home': 'index.md'}]
    
    # PQQ Drafts Section
    draft_files = sorted([f for f in os.listdir(DRAFTS_DIR) if f.endswith('.md') and f not in ['index.md', 'processed_log.md']])
    draft_nav = []
    for f in draft_files:
        title = os.path.splitext(f)[0].replace('_', ' ')
        draft_nav.append({title: f})
    if draft_nav:
        nav.append({'PQQ Drafts': draft_nav})
        
    # Evidence Library Section
    evidence_nav = []
    if os.path.exists(EVIDENCE_DEST_DIR):
        for dirname in sorted(os.listdir(EVIDENCE_DEST_DIR)):
            dirpath = os.path.join(EVIDENCE_DEST_DIR, dirname)
            if os.path.isdir(dirpath):
                category_title = dirname.replace('_', ' ').capitalize()
                category_files = sorted([f for f in os.listdir(dirpath) if f.endswith('.md')])
                category_nav = []
                for f in category_files:
                    title = os.path.splitext(f)[0].replace('_', ' ')
                    path = f"evidence_library/{dirname}/{f}"
                    category_nav.append({title: path})
                if category_nav:
                    evidence_nav.append({category_title: category_nav})
    if evidence_nav:
        nav.append({'Evidence Library': evidence_nav})

    # Processed Log Section
    nav.append({'Processed Log': 'processed_log.md'})
    
    return nav

def update_mkdocs_config(new_nav):
    """Reads mkdocs.yml, updates the nav section, and writes it back."""
    print(f"Updating '{MKDOCS_CONFIG_FILE}'...")
    with open(MKDOCS_CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    config['nav'] = new_nav
    
    with open(MKDOCS_CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f
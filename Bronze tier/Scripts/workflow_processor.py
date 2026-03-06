#!/usr/bin/env python3
"""
AI Employee Workflow Processor (Bronze Tier)
Handles file movement from Approved → Done, updates Dashboard, creates JSON logs.

Usage: python workflow_processor.py
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# Enable UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
VAULT_ROOT = Path(__file__).parent.parent  # Go up one level from Scripts/ to vault root
APPROVED_FOLDER = VAULT_ROOT / "Approved"
DONE_FOLDER = VAULT_ROOT / "Done"
LOGS_FOLDER = VAULT_ROOT / "Logs"
DASHBOARD_FILE = VAULT_ROOT / "Dashboard.md"
ACTIVITY_LOG = LOGS_FOLDER / "activity.json"

def ensure_folders():
    """Ensure all required folders exist."""
    for folder in [APPROVED_FOLDER, DONE_FOLDER, LOGS_FOLDER]:
        folder.mkdir(exist_ok=True)

def load_activity_log():
    """Load existing activity log or create new one."""
    if ACTIVITY_LOG.exists():
        with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"activities": [], "last_updated": None}

def save_activity_log(log_data):
    """Save activity log to JSON file."""
    log_data["last_updated"] = datetime.now().isoformat()
    with open(ACTIVITY_LOG, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

def parse_frontmatter(content):
    """Extract YAML-like frontmatter from markdown file."""
    frontmatter = {}
    lines = content.split('\n')
    in_frontmatter = False
    
    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                break
            continue
        
        if in_frontmatter and ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter

def process_approved_files():
    """Move approved files to Done and log the activity."""
    ensure_folders()
    log_data = load_activity_log()
    processed_count = 0
    
    if not APPROVED_FOLDER.exists():
        print("No Approved folder found.")
        return processed_count
    
    for file_path in APPROVED_FOLDER.glob("*.md"):
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            frontmatter = parse_frontmatter(content)
            
            # Extract metadata
            task_name = file_path.stem
            created = frontmatter.get('created', datetime.now().strftime('%Y-%m-%d'))
            category = frontmatter.get('category', 'General')
            value = frontmatter.get('value', '$0')
            priority = frontmatter.get('priority', 'Medium')
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "task_name": task_name,
                "category": category,
                "value": value,
                "priority": priority,
                "status": "Completed",
                "source_file": str(file_path.name),
                "action": "Moved from Approved to Done"
            }
            
            # Move file to Done folder
            # Add completion timestamp to frontmatter
            completion_marker = f"\n\n---\ncompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nprocessed_by: AI_Employee_Workflow_Processor_v0.1\n"
            
            new_content = content.rstrip() + completion_marker
            dest_path = DONE_FOLDER / file_path.name
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Remove from Approved
            file_path.unlink()
            
            # Add to activity log
            log_data["activities"].append(log_entry)

            print(f"[OK] Processed: {task_name} -> Done")
            processed_count += 1

        except Exception as e:
            print(f"[ERROR] Error processing {file_path.name}: {e}")
    
    # Save updated log
    save_activity_log(log_data)
    
    return processed_count

def update_dashboard(processed_count):
    """Update the Dashboard.md with recent activity."""
    if not DASHBOARD_FILE.exists():
        print("Dashboard.md not found. Skipping update.")
        return
    
    with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update timestamp
    today = datetime.now().strftime('%Y-%m-%d')
    content = content.replace('*Last Updated: [DATE]*', f'*Last Updated: {today}*')
    
    # Update Recent Activity section
    activity_entry = f"""
### {today} - Workflow Processing
- **Status:** ✅ Completed
- **Category:** Ops
- **Value:** N/A
- **Approval:** Auto
- **Notes:** Processed {processed_count} approved task(s) to Done

"""
    
    # Find the Recent Activity section and insert new entry
    if "<!-- AI Employee: Append new entries here (newest first) -->" in content:
        content = content.replace(
            "<!-- AI Employee: Append new entries here (newest first) -->",
            f"<!-- AI Employee: Append new entries here (newest first) -->\n{activity_entry}"
        )
    
    # Update task counts (simplified - just update the table)
    done_count = len(list(DONE_FOLDER.glob("*.md"))) if DONE_FOLDER.exists() else 0
    approved_count = len(list(APPROVED_FOLDER.glob("*.md"))) if APPROVED_FOLDER.exists() else 0
    
    # Update the Active Tasks Pipeline table
    old_pipeline = "| Done (Week) | 0 | - |"
    new_pipeline = f"| Done (Week) | {done_count} | - |"
    content = content.replace(old_pipeline, new_pipeline)
    
    old_approved = "| Approved | 0 | - |"
    new_approved = f"| Approved | {approved_count} | - |"
    content = content.replace(old_approved, new_approved)
    
    # Save updated dashboard
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📊 Dashboard updated.")

def main():
    """Main entry point."""
    print("=" * 50)
    print("AI Employee Workflow Processor v0.1")
    print("=" * 50)
    print()

    # Process approved files
    processed_count = process_approved_files()

    if processed_count == 0:
        print("No files to process in Approved folder.")
    else:
        print()
        # Update dashboard
        update_dashboard(processed_count)

    print()
    print("=" * 50)
    print(f"Processing complete. {processed_count} task(s) moved to Done.")
    print("=" * 50)

if __name__ == "__main__":
    main()

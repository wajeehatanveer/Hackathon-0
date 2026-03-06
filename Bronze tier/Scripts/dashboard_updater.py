#!/usr/bin/env python3
"""
AI Employee Dashboard Updater (Bronze Tier)
Updates Dashboard.md with metrics, activity, and status information.

Usage: python dashboard_updater.py [--full]
  --full: Recalculate all metrics from scratch
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

# Enable UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
VAULT_ROOT = Path(__file__).parent.parent
DASHBOARD_FILE = VAULT_ROOT / "Dashboard.md"
LOGS_FOLDER = VAULT_ROOT / "Logs"
DONE_FOLDER = VAULT_ROOT / "Done"
PENDING_FOLDER = VAULT_ROOT / "Pending_Approval"
NEEDS_ACTION_FOLDER = VAULT_ROOT / "Needs_Action"
PLANS_FOLDER = VAULT_ROOT / "Plans"
APPROVED_FOLDER = VAULT_ROOT / "Approved"

def count_markdown_files(folder):
    """Count .md files in a folder."""
    if not folder.exists():
        return 0
    return len(list(folder.glob("*.md")))

def load_activity_log():
    """Load activity log for metrics."""
    log_path = LOGS_FOLDER / "activity.json"
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"activities": []}

def get_week_range():
    """Get the current week's date range."""
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')

def calculate_weekly_stats():
    """Calculate statistics for the current week."""
    log_data = load_activity_log()
    week_start, _ = get_week_range()
    
    completed_this_week = 0
    for activity in log_data.get("activities", []):
        if activity.get("status") == "Completed":
            if activity.get("timestamp", "")[:10] >= week_start:
                completed_this_week += 1
    
    return completed_this_week

def calculate_monthly_stats():
    """Calculate statistics for the current month."""
    log_data = load_activity_log()
    current_month = datetime.now().strftime('%Y-%m')
    
    completed_this_month = 0
    auto_approved = 0
    hitl_required = 0
    
    for activity in log_data.get("activities", []):
        if activity.get("status") == "Completed":
            if activity.get("timestamp", "")[:7] == current_month:
                completed_this_month += 1
                # Could add more granular tracking here
    
    return completed_this_month, auto_approved, hitl_required

def parse_dashboard(content):
    """Parse dashboard into sections."""
    sections = {}
    current_section = "header"
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if line.startswith('## '):
            current_section = line
        if current_section not in sections:
            sections[current_section] = []
        sections[current_section].append((i, line))
    
    return sections

def update_dashboard():
    """Main dashboard update function."""
    if not DASHBOARD_FILE.exists():
        print(f"❌ Dashboard not found at {DASHBOARD_FILE}")
        return False
    
    with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    today = datetime.now().strftime('%Y-%m-%d')
    week_start, week_end = get_week_range()
    
    # Calculate counts
    needs_action_count = count_markdown_files(NEEDS_ACTION_FOLDER)
    plans_count = count_markdown_files(PLANS_FOLDER)
    pending_count = count_markdown_files(PENDING_FOLDER)
    approved_count = count_markdown_files(APPROVED_FOLDER)
    done_count = count_markdown_files(DONE_FOLDER)
    
    weekly_completed = calculate_weekly_stats()
    monthly_completed, auto_approved, hitl_required = calculate_monthly_stats()
    
    # Update Quick Stats table
    stats_table = f"""| Metric | Value | Trend |
|--------|-------|-------|
| Tasks Completed (Week) | {weekly_completed} | ➡️ |
| Tasks Completed (Month) | {monthly_completed} | ➡️ |
| Pending Approval | {pending_count} | ➡️ |
| Auto-Approved (Month) | {auto_approved} | ➡️ |
| HITL Required (Month) | {hitl_required} | ➡️ |"""
    
    # Simple replacement (could be more sophisticated)
    content = re.sub(
        r'\| Metric \| Value \| Trend \|\n\|--------\|-------\|-------\|.*?\| HITL Required \(Month\) \| \d+ \| ➡️ \|',
        stats_table,
        content,
        flags=re.DOTALL
    )
    
    # Update Active Tasks Pipeline table
    pipeline_table = f"""| Folder | Count | Oldest Item |
|--------|-------|-------------|
| Needs_Action | {needs_action_count} | - |
| Plans | {plans_count} | - |
| Pending_Approval | {pending_count} | - |
| Approved | {approved_count} | - |
| Done (Week) | {weekly_completed} | - |"""
    
    content = re.sub(
        r'\| Folder \| Count \| Oldest Item \|\n\|--------\|-------\|-------------\|.*?\| Done \(Week\) \| \d+ \| - \|',
        pipeline_table,
        content,
        flags=re.DOTALL
    )
    
    # Update timestamp
    content = content.replace("*Last Updated: [DATE]*", f"*Last Updated: {today}*")
    content = re.sub(r'\*Last Updated: \d{4}-\d{2}-\d{2}\*', f'*Last Updated: {today}*', content)
    
    # Update next auto-update
    next_update = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    content = content.replace("*Next auto-update: [DATE]*", f"*Next auto-update: {next_update}*")
    
    # Save updated dashboard
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Dashboard updated successfully!")
    print(f"   - Week: {week_start} to {week_end}")
    print(f"   - Tasks completed (week): {weekly_completed}")
    print(f"   - Pending approval: {pending_count}")
    print(f"   - Done folder: {done_count} total")
    
    return True

def main():
    """Main entry point."""
    print("=" * 50)
    print("AI Employee Dashboard Updater v0.1")
    print("=" * 50)
    print()
    
    success = update_dashboard()
    
    print()
    print("=" * 50)
    if success:
        print("Update complete!")
    else:
        print("Update failed. Check paths and try again.")
    print("=" * 50)

if __name__ == "__main__":
    main()

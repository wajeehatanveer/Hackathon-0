#!/usr/bin/env python3
"""
AI Employee JSON Logger (Bronze Tier)
Creates and maintains structured JSON logs for all AI Employee activities.

Usage:
  python json_logger.py log --task "Task Name" --category Finance --value 100 --status Completed
  python json_logger.py view [--today|--week|--month]
  python json_logger.py export --output report.json
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Enable UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
VAULT_ROOT = Path(__file__).parent.parent  # Go up one level from Scripts/ to vault root
LOGS_FOLDER = VAULT_ROOT / "Logs"
ACTIVITY_LOG = LOGS_FOLDER / "activity.json"

def ensure_log_exists():
    """Ensure the activity log file exists."""
    LOGS_FOLDER.mkdir(exist_ok=True)
    if not ACTIVITY_LOG.exists():
        with open(ACTIVITY_LOG, 'w', encoding='utf-8') as f:
            json.dump({"activities": [], "last_updated": None}, f, indent=2)

def load_log():
    """Load the activity log."""
    ensure_log_exists()
    with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_log(log_data):
    """Save the activity log."""
    log_data["last_updated"] = datetime.now().isoformat()
    with open(ACTIVITY_LOG, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

def log_activity(task_name, category, value, status, priority="Medium", 
                 approval_type="Auto", notes="", source_file=""):
    """Log a new activity entry."""
    log_data = load_log()
    
    entry = {
        "id": f"ACT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "task_name": task_name,
        "category": category,
        "value": str(value),
        "status": status,
        "priority": priority,
        "approval_type": approval_type,
        "notes": notes,
        "source_file": source_file
    }
    
    log_data["activities"].append(entry)
    save_log(log_data)
    
    print(f"✅ Logged: {task_name} ({status})")
    return entry

def view_activities(filter_type="all"):
    """View activities with optional filtering."""
    log_data = load_log()
    activities = log_data.get("activities", [])
    
    if not activities:
        print("📭 No activities logged yet.")
        return
    
    # Apply filters
    now = datetime.now()
    filtered = activities
    
    if filter_type == "today":
        today = now.strftime('%Y-%m-%d')
        filtered = [a for a in activities if a.get("timestamp", "")[:10] == today]
    elif filter_type == "week":
        week_start = (now - timedelta(days=now.weekday())).strftime('%Y-%m-%d')
        filtered = [a for a in activities if a.get("timestamp", "")[:10] >= week_start]
    elif filter_type == "month":
        current_month = now.strftime('%Y-%m')
        filtered = [a for a in activities if a.get("timestamp", "")[:7] == current_month]
    
    if not filtered:
        print(f"📭 No activities found for filter: {filter_type}")
        return
    
    # Display
    print(f"\n{'='*70}")
    print(f"Activity Log ({filter_type.upper()}) - {len(filtered)} entries")
    print(f"{'='*70}\n")
    
    for entry in reversed(filtered[-20:]):  # Show last 20
        timestamp = entry.get("timestamp", "N/A")[:19].replace('T', ' ')
        task = entry.get("task_name", "Unknown")
        status = entry.get("status", "Unknown")
        value = entry.get("value", "$0")
        category = entry.get("category", "General")
        
        status_icon = {"Completed": "✅", "Pending": "⏳", "Blocked": "⚠️"}.get(status, "📝")
        
        print(f"{timestamp} | {status_icon} {task}")
        print(f"    Category: {category} | Value: {value} | Priority: {entry.get('priority', 'Medium')}")
        if entry.get("notes"):
            print(f"    Notes: {entry['notes']}")
        print()

def export_log(output_file):
    """Export log to a new JSON file."""
    log_data = load_log()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Exported to: {output_file}")

def calculate_summary():
    """Calculate and display summary statistics."""
    log_data = load_log()
    activities = log_data.get("activities", [])
    
    if not activities:
        print("📭 No activities to summarize.")
        return
    
    total = len(activities)
    completed = len([a for a in activities if a.get("status") == "Completed"])
    pending = len([a for a in activities if a.get("status") == "Pending"])
    
    # Category breakdown
    categories = {}
    for a in activities:
        cat = a.get("category", "General")
        categories[cat] = categories.get(cat, 0) + 1
    
    # Value tracking (attempt to parse $ values)
    total_value = 0
    for a in activities:
        value_str = a.get("value", "$0")
        try:
            value = float(value_str.replace('$', '').replace(',', ''))
            total_value += value
        except:
            pass
    
    print(f"\n{'='*50}")
    print("📊 ACTIVITY SUMMARY")
    print(f"{'='*50}")
    print(f"Total Activities: {total}")
    print(f"Completed: {completed}")
    print(f"Pending: {pending}")
    print(f"Total Value Tracked: ${total_value:.2f}")
    print(f"\nBy Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count}")
    print(f"{'='*50}\n")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI Employee JSON Logger")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Log command
    log_parser = subparsers.add_parser("log", help="Log a new activity")
    log_parser.add_argument("--task", required=True, help="Task name")
    log_parser.add_argument("--category", default="General", help="Category")
    log_parser.add_argument("--value", default="$0", help="Value (e.g., $100)")
    log_parser.add_argument("--status", default="Completed", help="Status")
    log_parser.add_argument("--priority", default="Medium", help="Priority")
    log_parser.add_argument("--approval", default="Auto", help="Approval type")
    log_parser.add_argument("--notes", default="", help="Notes")
    
    # View command
    view_parser = subparsers.add_parser("view", help="View activities")
    view_parser.add_argument("--today", action="store_true", help="Show today only")
    view_parser.add_argument("--week", action="store_true", help="Show this week")
    view_parser.add_argument("--month", action="store_true", help="Show this month")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export log")
    export_parser.add_argument("--output", required=True, help="Output file path")
    
    # Summary command
    subparsers.add_parser("summary", help="Show summary statistics")
    
    args = parser.parse_args()
    
    if args.command == "log":
        ensure_log_exists()
        log_activity(
            task_name=args.task,
            category=args.category,
            value=args.value,
            status=args.status,
            priority=args.priority,
            approval_type=args.approval,
            notes=args.notes
        )
    elif args.command == "view":
        if args.today:
            view_activities("today")
        elif args.week:
            view_activities("week")
        elif args.month:
            view_activities("month")
        else:
            view_activities("all")
    elif args.command == "export":
        export_log(args.output)
    elif args.command == "summary":
        calculate_summary()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

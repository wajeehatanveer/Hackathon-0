# 🚀 SETUP GUIDE - Personal AI Employee (Bronze Tier)

## Quick Start (5 Minutes)

### Step 1: Verify Folder Structure ✅

Your vault should now have these folders:
```
AI_Employee_Vault/
├── Needs_Action/      ← Drop new tasks here
├── Plans/             ← AI-generated plans stored here
├── Pending_Approval/  ← Awaiting human decision
├── Approved/          ← Approved, ready to process
├── Done/              ← Completed tasks archive
├── Logs/              ← JSON activity logs
├── Briefings/         ← Executive briefings
├── Skill_Templates/   ← Reusable Qwen prompts
└── Scripts/           ← Python automation
```

**NEXT ACTION:** In Obsidian, verify all folders exist in left sidebar.

---

### Step 2: Verify Template Files ✅

Root files created:
- `Business_Goals.md` - Your 2026 targets
- `Company_Handbook.md` - Rules and thresholds
- `Dashboard.md` - Live activity overview
- `Qwen_AI_Employee_System_Prompt.md` - Main Qwen prompt

**NEXT ACTION:** Open each file in Obsidian, review contents.

---

### Step 3: Python Setup (Optional but Recommended) ✅

The automation scripts enhance the workflow but are optional.

#### Check Python Installation
```bash
python --version
```

If not installed: Download from https://python.org (check "Add to PATH")

#### No Additional Packages Required
Scripts use only Python standard library (os, json, datetime, pathlib).

#### Test Scripts
```bash
cd "C:\Users\hp\OneDrive\Documents\Hackathon 0\AI_Employee_Vault\Scripts"
python json_logger.py summary
```

Expected output: "No activities to summarize" (empty log is normal)

**NEXT ACTION:** Run test command above. If error, check Python installation.

---

### Step 4: Configure Your Goals ✅

Edit `Business_Goals.md` with YOUR actual goals:

1. Update revenue target
2. Modify projects list
3. Adjust subscription audit rules
4. Set your quarterly goals

**NEXT ACTION:** Open `Business_Goals.md`, replace dummy data with real goals.

---

### Step 5: Configure Your Handbook ✅

Edit `Company_Handbook.md` with YOUR rules:

1. Adjust approval thresholds (default: ≤$10 auto, >$50 HITL)
2. Add your sensitive action types
3. Set your quality standards
4. Update review schedules

**NEXT ACTION:** Open `Company_Handbook.md`, customize thresholds and rules.

---

## 📖 How to Use (Workflow)

### Creating a New Task

1. **In Obsidian:** Create new file in `/Needs_Action/`
2. **Name:** `TASK_YYYYMMDD_Description.md`
3. **Use template:**
```markdown
---
created: 2026-01-15
priority: Medium
category: Finance
estimated_value: $50
---

# Task: [Task Name]

## Description
[What needs to be done]

## Details
- **Specifics:** [Details]
- **Deadline:** [Date]
- **Contact:** [If applicable]

## AI Employee Instructions
[Any specific guidance for Qwen]
```

**NEXT ACTION:** Create your first task file.

---

### Processing a Task with Qwen

1. **Open task file** in Obsidian
2. **Select All** (Ctrl+A) and **Copy** (Ctrl+C)
3. **Open Qwen chat** (web or app)
4. **Paste System Prompt** from `Qwen_AI_Employee_System_Prompt.md`
5. **Paste task content** below the prompt
6. **Send to Qwen**
7. **Copy Qwen's output**
8. **Save to appropriate folder:**
   - Plan → `/Plans/PLAN_xxx.md`
   - Approval needed → `/Pending_Approval/APPROVAL_xxx.md`
   - Auto-approve → Execute + log

**NEXT ACTION:** Try with the example task in `/Needs_Action/example_task.md`

---

### Approval Workflow

When Qwen generates a Pending_Approval file:

1. **Save** output to `/Pending_Approval/`
2. **Review** the approval request in Obsidian
3. **Check** YES, NO, or MODIFY box
4. **Add notes** if modifying
5. **Move file** to `/Approved/` (if approved)
6. **Run script:** `python workflow_processor.py`
7. **Task moves** to `/Done/` + Dashboard updates

---

### Running Automation Scripts

#### Option 1: Process Approved Tasks
```bash
cd "C:\Users\hp\OneDrive\Documents\Hackathon 0\AI_Employee_Vault\Scripts"
python workflow_processor.py
```

#### Option 2: Update Dashboard
```bash
cd "C:\Users\hp\OneDrive\Documents\Hackathon 0\AI_Employee_Vault\Scripts"
python dashboard_updater.py
```

#### Option 3: Manual Logging
```bash
cd "C:\Users\hp\OneDrive\Documents\Hackathon 0\AI_Employee_Vault\Scripts"
python json_logger.py log --task "My Task" --category Finance --value 100
```

#### Option 4: View Activity
```bash
python json_logger.py view --week
python json_logger.py summary
```

---

## 🎯 Using Skill Templates

### When to Use Each Skill

| Skill | Use When | Output |
|-------|----------|--------|
| **Planning** | Need step-by-step guidance | `/Plans/PLAN_xxx.md` |
| **Approval** | Need to check thresholds | `/Pending_Approval/APPROVAL_xxx.md` |
| **Briefing** | Need executive summary | `/Briefings/BRIEF_xxx.md` |
| **Full Process** | Standard task processing | Multiple outputs |

### How to Use Skills

1. **Open** skill template from `/Skill_Templates/`
2. **Copy** the prompt section
3. **Paste to Qwen** with your task content
4. **Save** output to suggested folder

---

## 📁 File Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Tasks | `TASK_YYYYMMDD_Description.md` | `TASK_20260115_SendInvoice.md` |
| Plans | `PLAN_YYYYMMDD_Description.md` | `PLAN_20260115_SendInvoice.md` |
| Approvals | `APPROVAL_YYYYMMDD_Description.md` | `APPROVAL_20260115_ClientDiscount.md` |
| Briefings | `BRIEF_YYYYMMDD_Topic.md` | `BRIEF_20260115_ContractRenewal.md` |

---

## 🔧 Troubleshooting

### Script Error: "Python not found"
**Fix:** Install Python from python.org, restart terminal

### Script Error: "File not found"
**Fix:** Run scripts from `/Scripts/` directory or use full paths

### Qwen output unclear
**Fix:** Add more detail to task, paste Business_Goals and Handbook

### Dashboard not updating
**Fix:** Run `dashboard_updater.py` after processing

### Approval file not moving
**Fix:** Manually move from `/Pending_Approval/` to `/Approved/` after checking YES

---

## 📊 Example End-to-End Flow

```
1. Create: /Needs_Action/TASK_20260115_Invoice.md
   └─ "Send $80 invoice to Client X"

2. Qwen Process: Paste to Qwen chat
   └─ Returns: "HITL required (>$50)"
   └─ Returns: Pending_Approval content

3. Save: /Pending_Approval/APPROVAL_20260115_Invoice.md

4. Human Review: Open in Obsidian
   └─ Check: [x] APPROVE
   └─ Sign: "John Doe, 2026-01-15"

5. Move: To /Approved/ folder

6. Run: python workflow_processor.py
   └─ Moves to /Done/
   └─ Updates Dashboard
   └─ Logs to activity.json

7. Complete! ✅
```

---

## 🎓 Best Practices

### Do ✅
- Create tasks with clear descriptions
- Include estimated values for threshold checking
- Review Qwen output before saving
- Run scripts after approval workflow
- Update goals quarterly

### Don't ❌
- Skip the approval workflow for sensitive items
- Modify files outside the vault without approval
- Delete logs (archive instead)
- Process tasks without Qwen review (defeats the purpose)

---

## 📞 Support

### Hackathon Resources
- Check hackathon docs for Bronze Tier requirements
- Review rubric for scoring criteria
- Test all workflow steps before submission

### Self-Help
1. Re-read `Company_Handbook.md` for rules
2. Check `Qwen_AI_Employee_System_Prompt.md` for Qwen usage
3. Review skill templates for specific scenarios

---

## ✅ Setup Checklist

- [ ] All folders created
- [ ] All template files present
- [ ] Python installed and tested
- [ ] Business_Goals.md customized
- [ ] Company_Handbook.md customized
- [ ] Example task processed successfully
- [ ] Scripts tested
- [ ] First real task created and processed

---

*Setup Guide Version: 1.0*
*Bronze Tier - Personal AI Employee*
*Powered by Qwen*

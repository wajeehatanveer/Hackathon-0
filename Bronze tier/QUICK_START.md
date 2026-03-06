# ⚡ QUICK START - Personal AI Employee

## 60-Second Overview

**What this is:** A Qwen-powered AI employee that processes tasks from your Obsidian vault following strict approval rules.

**What you need:** Obsidian + Qwen chat (web or app) + Optional Python for automation

---

## First Task (2 Minutes)

### 1. Open Example Task
In Obsidian, open: `Needs_Action/example_task.md`

### 2. Copy Content
Select all (Ctrl+A) → Copy (Ctrl+C)

### 3. Open Qwen Chat
Go to your Qwen interface

### 4. Paste System Prompt
Open `Qwen_AI_Employee_System_Prompt.md`, copy the entire prompt block, paste to Qwen.

### 5. Paste Task
Below the system prompt, paste the example task content.

### 6. Send to Qwen
Wait for structured output.

### 7. Save Output
Qwen will say this needs approval (>$50). Save the Pending_Approval content to:
`Pending_Approval/APPROVAL_20260115_Invoice.md`

**Done!** You've processed your first task.

---

## Approve Task (1 Minute)

### 1. Open Approval File
In Obsidian: `Pending_Approval/APPROVAL_20260115_Invoice.md`

### 2. Make Decision
Check the box:
```
- [x] **APPROVE** - Proceed with action
```

### 3. Add Signature
```
- **Approved by:** Your Name
- **Date:** 2026-01-15
```

### 4. Move File
Drag from `Pending_Approval/` to `Approved/`

---

## Complete Workflow (30 Seconds)

### Run Python Script
```bash
cd "C:\Users\hp\OneDrive\Documents\Hackathon 0\AI_Employee_Vault\Scripts"
python workflow_processor.py
```

**What happens:**
- ✅ File moves to `/Done/`
- ✅ Dashboard updates
- ✅ JSON log created

### No Python? Manual Complete
1. Move file from `Approved/` to `Done/`
2. Open `Dashboard.md`, add entry to Recent Activity
3. Open `Logs/activity.json`, add log entry (create if needed)

---

## Your Turn: Create New Task

### Template (Copy-Paste)
```markdown
---
created: 2026-01-15
priority: Medium
category: Finance
estimated_value: $25
---

# Task: [Task Name]

## Description
[What needs to be done]

## Details
- **Specifics:** [Details]
- **Deadline:** [Date]

## AI Employee Instructions
[Any guidance for Qwen]
```

### Save To
`Needs_Action/TASK_YYYYMMDD_Description.md`

---

## Qwen Prompt Quick Reference

### Full Processing (Default)
```
[Paste system prompt from Qwen_AI_Employee_System_Prompt.md]
[Paste task content]
```

### Planning Only
```
[Paste system prompt]
SKILL MODE: Planning Only
[Paste task content]
```

### Approval Check Only
```
[Paste system prompt]
SKILL MODE: Approval Check Only
[Paste task content]
```

### Briefing Only
```
[Paste system prompt]
SKILL MODE: Briefing Generation
[Paste task content]
```

---

## Approval Thresholds (Memorize These)

| Value | Decision |
|-------|----------|
| ≤$10 | ✅ Auto-approve |
| $10-$50 | 📝 Log + notify |
| >$50 | ⚠️ Human approval |
| Sensitive* | ⚠️ Always approve |

*Sensitive = passwords, legal, bank, contracts, data deletion

---

## Folder Workflow

```
Needs_Action     →  Qwen Processing  →  Plans/Pending_Approval
                                              ↓
Pending_Approval →  Human Decision   →  Approved
                                              ↓
Approved         →  Script/Manual    →  Done + Dashboard + Log
```

---

## Scripts Quick Reference

| Command                                           | What It Does            |
| ------------------------------------------------- | ----------------------- |
| `python workflow_processor.py`                    | Process Approved → Done |
| `python dashboard_updater.py`                     | Refresh Dashboard       |
| `python json_logger.py log --task "X" --value 50` | Manual log              |
| `python json_logger.py view --week`               | View this week          |
| `python json_logger.py summary`                   | Show statistics         |
|                                                   |                         |

---

## Common Scenarios

### Scenario 1: Send $5 Invoice
**Flow:** Create → Qwen → Auto-approve → Execute → Log → Done

### Scenario 2: Approve $100 Expense
**Flow:** Create → Qwen → Pending_Approval → Human YES → Approved → Done

### Scenario 3: Plan New Project
**Flow:** Create → Qwen (Planning Skill) → Save Plan → Execute Plan → Done

### Scenario 4: Decision Briefing
**Flow:** Create → Qwen (Briefing Skill) → Human Decision → Execute → Done

---

## Dashboard Quick Update

If not using scripts, manually add to `Dashboard.md`:

```markdown
### 2026-01-15 - [Task Name]
- **Status:** ✅ Completed
- **Category:** Finance/Ops/Client/Admin
- **Value:** $X
- **Approval:** Auto / HITL
- **Notes:** Brief description
```

---

## Tips for Success

1. **Be specific** in task descriptions
2. **Always include value** for threshold checking
3. **Review Qwen output** before saving
4. **Follow the workflow** - don't skip approval
5. **Run scripts** or update manually after completion

---

## Next Steps

1. ✅ Process the example task (done above)
2. ✅ Create your first real task
3. ✅ Customize `Business_Goals.md`
4. ✅ Customize `Company_Handbook.md`
5. ✅ Read full `SETUP_GUIDE.md` when ready

---

**Need Help?** Open `SETUP_GUIDE.md` for detailed instructions.

*Quick Start Version: 1.0*
*Bronze Tier - Personal AI Employee*

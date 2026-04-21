# GitHub Branch Comparison Agent - Quick Start Guide

## 🚀 Setup Complete!

The Branch Comparison Agent has been successfully integrated into your repository. Here's how to use it:

## Quick Usage

### Method 1: GitHub Actions (Recommended for CI/CD)

1. **Push your changes to GitHub** (if not already done)
   ```bash
   git push origin main
   git push origin QA1
   ```

2. **Trigger the workflow**:
   - Go to: **GitHub Repository → Actions**
   - Select: **"Branch Comparison Agent"** workflow
   - Click: **"Run workflow"**
   - (Optional) Change branch names if needed
   - Click: **"Run workflow"**

3. **View Results**:
   - The workflow will generate reports as artifacts
   - Reports are also committed to the repo in `/reports` directory
   - Latest report always available as:
     - `reports/latest_comparison.md` (Markdown)
     - `reports/latest_comparison.json` (JSON)

### Method 2: Local Command Line

Run directly on your machine:

```bash
# Navigate to repo root
cd c:\Users\suman\OneDrive\Documents\GitHub\Pic-Upload-Api

# Run the comparison (default: main vs QA1)
python PictureUpload\scripts\branch_comparison_agent.py . main QA1

# Or with custom branches
python PictureUpload\scripts\branch_comparison_agent.py . branch1 branch2
```

## 📊 What You Get

### Markdown Report (`latest_comparison.md`)
- Summary table with file counts
- List of files missing in QA1
- List of files added in QA1
- Detailed diffs for modified files
- Human-readable format

### JSON Report (`latest_comparison.json`)
- Structured data format
- Programmatically parseable
- Useful for integrations
- Includes timestamps and metadata

## 📁 Repository Structure

```
Pic-Upload-Api/
├── .github/
│   └── workflows/
│       └── branch-comparison.yml    ← GitHub Actions workflow
├── PictureUpload/
│   ├── scripts/
│   │   └── branch_comparison_agent.py    ← Main comparison script
│   └── reports/                          ← Reports stored here
├── reports/                              ← Also here (at repo root)
│   ├── latest_comparison.md
│   ├── latest_comparison.json
│   └── comparison_report_*.{md,json}    ← Timestamped archives
└── BRANCH_COMPARISON_AGENT.md           ← Full documentation
```

## 🔧 Current Configuration

- **Branch 1** (baseline/production): `main`
- **Branch 2** (development): `QA1`
- **Report Location**: `/reports` (repo root)
- **Trigger**: Manual via GitHub Actions

## 📝 Example Report Output

```
# GitHub Branch Comparison Report

**Generated**: 2026-04-21 21:44:00
**Comparison**: `main` <-> `QA1`

## Summary
| Metric | Count |
|--------|-------|
| Files in main | 30 |
| Files in QA1 | 28 |
| Common Files | 28 |
| Missing in QA1 | 2 |
| Modified Files | 1 |

## Files Missing in `QA1`
- `.github/workflows/branch-compare.yml`
- `compare.py`

## Modified Files
### Image.java
[Shows detailed diffs...]
```

## ⚙️ Customization Options

### Change Default Branches

Edit `.github/workflows/branch-comparison.yml`:

```yaml
branch1:
  default: 'main'      # Change this
branch2:
  default: 'QA1'       # Or this
```

### Schedule Automatic Comparisons

Add to workflow:

```yaml
on:
  schedule:
    - cron: '0 9 * * MON'  # Every Monday at 9 AM UTC
```

### Send Notifications

Add Slack, Email, or Teams notifications in the workflow.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Branch not found" | Run `git fetch origin` first |
| Empty reports | Check branches are different |
| Encoding errors | Python script automatically handles these |
| Reports not appearing | Check GitHub Actions logs |

## 📚 Full Documentation

See [BRANCH_COMPARISON_AGENT.md](BRANCH_COMPARISON_AGENT.md) for:
- Advanced usage
- Integration examples
- API details
- Scheduling options
- Slack/Email notifications setup

## 🎯 Next Steps

1. ✅ **Setup Complete** - Agent is ready to use
2. 🔄 **First Comparison** - Run via GitHub Actions or locally
3. 📊 **Review Report** - Check `/reports/latest_comparison.md`
4. 🔧 **Customize** - Adjust branches or schedule as needed

## 💡 Tips

- Reports are **versioned** with timestamps for easy archival
- **Latest** reports are always available as `latest_comparison.*`
- Works with any branch combination (not just main/QA1)
- Perfect for validating QA environments before production releases

---

**Questions?** Check the full documentation or review GitHub Actions logs for detailed execution info.

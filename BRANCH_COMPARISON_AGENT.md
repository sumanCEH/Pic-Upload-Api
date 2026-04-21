# Branch Comparison Agent

A GitHub automation agent that compares two branches (typically `master` and `QA`) and generates comprehensive, step-by-step reports highlighting all differences.

## Features

✅ **File Presence Comparison**
- Detects files that exist in one branch but not the other
- Lists missing files (present in master but absent in QA)
- Lists additional files (present in QA but absent in master)

✅ **File Content Analysis**
- Identifies differences in code, methods, and logic
- Generates detailed diffs for modified files
- Provides line-by-line change information

✅ **Comprehensive Reporting**
- **Markdown Reports**: Human-readable, formatted for easy review
- **JSON Reports**: Structured data for programmatic access
- **Artifacts**: Automatically uploaded to GitHub Actions

✅ **Easy Automation**
- Manually triggered via GitHub Actions workflow
- Can be scheduled for periodic comparisons
- Supports custom branch selection

## Usage

### Option 1: GitHub Actions (Recommended)

1. **Manual Trigger**:
   - Go to your repository's **Actions** tab
   - Select **"Branch Comparison Agent"** workflow
   - Click **"Run workflow"**
   - (Optional) Specify custom branches (defaults to `master` and `QA`)
   - Click **"Run workflow"**

2. **View Results**:
   - Check the workflow run output for a summary
   - Download the **"comparison-reports"** artifact
   - Reports are saved as:
     - `reports/latest_comparison.md` (most recent)
     - `reports/latest_comparison.json` (structured format)
     - Timestamped versions for archival

### Option 2: Local Execution

Run the Python script directly on your machine:

```bash
cd PictureUpload
python scripts/branch_comparison_agent.py . master QA
```

**Arguments**:
- `[repo_path]`: Path to Git repository (default: current directory)
- `[branch1]`: First branch to compare (default: `master`)
- `[branch2]`: Second branch to compare (default: `QA`)

## Report Format

### Markdown Report (`latest_comparison.md`)

```markdown
# GitHub Branch Comparison Report

**Generated**: 2026-04-21 10:30:45
**Comparison**: `master` ↔ `QA`

## Summary
| Metric | Count |
|--------|-------|
| Files in master | 50 |
| Files in QA | 52 |
| Common Files | 48 |
| Missing in QA | 2 |
| Additional in QA | 4 |
| Modified Files | 15 |

## Files Missing in `QA` (Present in `master`)
- `src/old-feature.java`
- `src/deprecated-util.java`

## Files Additional in `QA` (Not in `master`)
- `src/new-feature.java`
- `src/experiment.java`

## Modified Files (Differences Between Branches)
### 1. `src/main/java/com/suman/controller/ClientController.java`
```diff
@@ -1,5 +1,6 @@
 public class ClientController {
-    public void oldMethod() {}
+    public void newMethod() {}
 }
```
```

### JSON Report (`latest_comparison.json`)

```json
{
  "timestamp": "2026-04-21T10:30:45.123456",
  "comparison": {
    "branch1": "master",
    "branch2": "QA"
  },
  "summary": {
    "total_files_branch1": 50,
    "total_files_branch2": 52,
    "common_files": 48,
    "missing_in_branch2": 2,
    "additional_in_branch2": 4,
    "modified_files": 15
  },
  "details": {
    "missing_in_branch2": ["src/old-feature.java"],
    "additional_in_branch2": ["src/new-feature.java"],
    "modified_files": ["src/main/java/com/suman/controller/ClientController.java"]
  }
}
```

## Requirements

- **GitHub Actions**: Enabled in your repository
- **Python**: 3.7+ (for local execution)
- **Git**: Installed and configured
- **Write Access**: To repository (if committing reports)

## How It Works

1. **Fetch Branches**: Automatically fetches the latest from remote
2. **Enumerate Files**: Lists all tracked files in both branches
3. **Categorize Differences**:
   - Missing files (in branch1 but not branch2)
   - Additional files (in branch2 but not branch1)
   - Modified files (present in both, but different content)
4. **Generate Diffs**: Creates detailed diffs for all modified files
5. **Report Generation**: Produces both Markdown and JSON reports
6. **Store Reports**: Saves to `/reports` directory with timestamps

## Directory Structure

```
PictureUpload/
├── scripts/
│   └── branch_comparison_agent.py      # Main comparison script
└── reports/
    ├── latest_comparison.md             # Most recent markdown report
    ├── latest_comparison.json           # Most recent JSON report
    ├── comparison_report_20260421_103045.md
    └── comparison_report_20260421_103045.json
```

## Advanced Usage

### Scheduling Automatic Comparisons

Edit `.github/workflows/branch-comparison.yml` and add a schedule:

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 9 * * MON'  # Every Monday at 9 AM UTC
```

### Custom Branches

You can compare any branches, not just `master` and `QA`:

```bash
python scripts/branch_comparison_agent.py . develop feature/new-api
```

### Sending Notifications

You can extend the workflow to send reports via:
- Email
- Slack
- Teams
- Email notifications (GitHub built-in)

## Troubleshooting

### "Not a Git repository"
Ensure the script is run from within a Git repository directory.

### "Branch not found"
Ensure both branches exist on the remote repository:
```bash
git fetch origin
git branch -a
```

### Empty Report
- Check that the branches have actual differences
- Verify the branch names are correct
- Ensure files are tracked by Git (not in `.gitignore`)

## Integration Examples

### With Pull Requests

Automatically comment on PRs with a comparison summary:

```yaml
- name: Comment on PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const report = fs.readFileSync('PictureUpload/reports/latest_comparison.md', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '## Branch Comparison\n' + report
      });
```

### Slack Notifications

Add a Slack notification step:

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Branch comparison report generated",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "View the [comparison report]()"
            }
          }
        ]
      }
```

## Future Enhancements

- [ ] Generate PDF reports
- [ ] Add code metrics comparison (lines of code, complexity)
- [ ] Integration with GitHub Issues/Projects
- [ ] Performance metrics
- [ ] Automatic PR generation for critical changes
- [ ] Email summaries with attachments

## License

This agent is part of the Pic-Upload-Api project.

---

**Questions or Issues?** Create an issue in the repository or check the GitHub Actions logs for detailed execution information.

import subprocess
import html

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# Get summary (file-level)
summary = run_command("git diff --name-status origin/main origin/QA1")

# Get detailed diff (line-level)
diff = run_command("git diff origin/main origin/QA1")

# Escape HTML (important to avoid breaking UI)
summary_html = html.escape(summary)
diff_html = html.escape(diff)

# Build HTML report
html_content = f"""
<html>
<head>
    <title>Branch Comparison Report</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        h1 {{ color: #333; }}
        pre {{
            background: #f4f4f4;
            padding: 10px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>

<h1>Branch Comparison Report</h1>
<h2>Main vs QA1</h2>

<h3>📁 File Summary</h3>
<pre>{summary_html}</pre>

<h3>🧾 Detailed Code Changes</h3>
<pre>{diff_html}</pre>

</body>
</html>
"""

# Write report
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTML report generated successfully!")
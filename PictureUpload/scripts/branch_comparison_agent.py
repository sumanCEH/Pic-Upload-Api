#!/usr/bin/env python3
"""
GitHub Branch Comparison Agent
Compares master and QA branches to generate a comprehensive difference report.
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import difflib

class BranchComparisonAgent:
    """Agent to compare two Git branches and generate detailed reports."""
    
    def __init__(self, repo_path: str, branch1: str = "master", branch2: str = "QA"):
        """
        Initialize the comparison agent.
        
        Args:
            repo_path: Path to the Git repository
            branch1: First branch to compare (typically production)
            branch2: Second branch to compare (typically development)
        """
        self.repo_path = Path(repo_path)
        self.branch1 = branch1
        self.branch2 = branch2
        self.report_dir = self.repo_path / "reports"
        self.report_dir.mkdir(exist_ok=True)
        
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a Git repository: {repo_path}")
    
    def run_git_command(self, command: str) -> str:
        """Execute a git command and return output."""
        try:
            result = subprocess.run(
                f"git -C {self.repo_path} {command}",
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e.stderr}")
            return ""
    
    def get_files_in_branch(self, branch: str) -> Set[str]:
        """Get all tracked files in a branch."""
        try:
            output = self.run_git_command(f"ls-tree -r --name-only {branch}")
            return set(output.split('\n')) if output else set()
        except Exception as e:
            print(f"Error getting files from {branch}: {e}")
            return set()
    
    def get_file_content(self, branch: str, file_path: str) -> str:
        """Get the content of a file from a specific branch."""
        try:
            output = self.run_git_command(f"show {branch}:{file_path}")
            return output
        except Exception as e:
            return ""
    
    def get_file_diff(self, file_path: str) -> str:
        """Get the diff for a file between two branches."""
        try:
            output = self.run_git_command(
                f"diff {self.branch1}..{self.branch2} -- {file_path}"
            )
            return output
        except Exception as e:
            return ""
    
    def compare_branches(self) -> Dict:
        """Compare the two branches and categorize differences."""
        print(f"Fetching branches: {self.branch1} and {self.branch2}...")
        
        # Ensure branches exist
        self.run_git_command("fetch origin")
        
        files_branch1 = self.get_files_in_branch(self.branch1)
        files_branch2 = self.get_files_in_branch(self.branch2)
        
        print(f"Files in {self.branch1}: {len(files_branch1)}")
        print(f"Files in {self.branch2}: {len(files_branch2)}")
        
        # Categorize differences
        missing_in_branch2 = files_branch1 - files_branch2  # In branch1 but not branch2
        additional_in_branch2 = files_branch2 - files_branch1  # In branch2 but not branch1
        common_files = files_branch1 & files_branch2  # In both branches
        
        # Check for modified files in common files
        modified_files = {}
        for file_path in common_files:
            diff = self.get_file_diff(file_path)
            if diff:  # File has differences
                modified_files[file_path] = diff
        
        return {
            "missing_in_branch2": sorted(list(missing_in_branch2)),
            "additional_in_branch2": sorted(list(additional_in_branch2)),
            "modified_files": modified_files,
            "total_files_branch1": len(files_branch1),
            "total_files_branch2": len(files_branch2),
            "common_files_count": len(common_files),
            "modified_count": len(modified_files)
        }
    
    def generate_markdown_report(self, comparison_data: Dict) -> str:
        """Generate a comprehensive, easy-to-understand Markdown report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = []
        
        # Header
        report.append("# BRANCH COMPARISON REPORT\n\n")
        report.append(f"Generated: {timestamp}\n")
        report.append(f"Comparing: [{self.branch1}] vs [{self.branch2}]\n")
        report.append("\n" + "="*80 + "\n\n")
        
        # Quick Summary Box
        report.append("QUICK SUMMARY\n")
        report.append("-" * 80 + "\n")
        report.append(f"Total Files in {self.branch1}: {comparison_data['total_files_branch1']}\n")
        report.append(f"Total Files in {self.branch2}: {comparison_data['total_files_branch2']}\n")
        report.append(f"Common Files: {comparison_data['common_files_count']}\n")
        report.append(f"Missing in {self.branch2}: {len(comparison_data['missing_in_branch2'])} file(s)\n")
        report.append(f"New in {self.branch2}: {len(comparison_data['additional_in_branch2'])} file(s)\n")
        report.append(f"Modified Files: {comparison_data['modified_count']} file(s)\n")
        report.append("-" * 80 + "\n\n")
        
        # Status Indicators
        report.append("STATUS OVERVIEW\n")
        report.append("-" * 80 + "\n")
        
        if comparison_data['missing_in_branch2']:
            report.append(f"[!] IMPORTANT: {len(comparison_data['missing_in_branch2'])} file(s) are missing from {self.branch2}\n")
            report.append(f"    These files exist in {self.branch1} but NOT in {self.branch2}\n\n")
        else:
            report.append(f"[OK] {self.branch2} contains all files from {self.branch1}\n\n")
        
        if comparison_data['additional_in_branch2']:
            report.append(f"[*] {self.branch2} has {len(comparison_data['additional_in_branch2'])} new file(s)\n")
            report.append(f"    These files are in {self.branch2} but NOT in {self.branch1}\n\n")
        else:
            report.append(f"[OK] No new files in {self.branch2}\n\n")
        
        if comparison_data['modified_count']:
            report.append(f"[~] {comparison_data['modified_count']} file(s) have code changes\n")
            report.append(f"    These files exist in both branches but with different content\n\n")
        else:
            report.append(f"[OK] No code changes in common files\n\n")
        
        report.append("\n" + "="*80 + "\n\n")
        
        # Files Missing in Branch 2
        if comparison_data['missing_in_branch2']:
            report.append("FILES MISSING FROM " + self.branch2.upper() + "\n")
            report.append("-" * 80 + "\n")
            report.append(f"Total: {len(comparison_data['missing_in_branch2'])} file(s)\n")
            report.append(f"Action: These files need to be added to {self.branch2}\n\n")
            
            for i, file_path in enumerate(comparison_data['missing_in_branch2'], 1):
                report.append(f"  {i}. {file_path}\n")
            report.append("\n")
        
        # Files Additional in Branch 2
        if comparison_data['additional_in_branch2']:
            report.append("NEW FILES IN " + self.branch2.upper() + "\n")
            report.append("-" * 80 + "\n")
            report.append(f"Total: {len(comparison_data['additional_in_branch2'])} file(s)\n")
            report.append(f"Status: These are new files added to {self.branch2}\n\n")
            
            for i, file_path in enumerate(comparison_data['additional_in_branch2'], 1):
                report.append(f"  {i}. {file_path}\n")
            report.append("\n")
        
        # Modified Files with detailed diffs
        if comparison_data['modified_files']:
            report.append("MODIFIED FILES (CODE CHANGES)\n")
            report.append("-" * 80 + "\n")
            report.append(f"Total: {comparison_data['modified_count']} file(s)\n\n")
            
            for idx, (file_path, diff_content) in enumerate(comparison_data['modified_files'].items(), 1):
                report.append(f"\n{idx}. {file_path}\n")
                report.append("   " + "-" * 76 + "\n")
                
                # Count added/removed lines
                added_lines = diff_content.count('\n+') - 1
                removed_lines = diff_content.count('\n-') - 1
                
                report.append(f"   Changes: {removed_lines} lines removed, {added_lines} lines added\n\n")
                report.append("   " + "=" * 76 + "\n")
                report.append("   DETAILED DIFF:\n")
                report.append("   " + "=" * 76 + "\n\n")
                
                # Limit diff output
                diff_lines = diff_content.split('\n')[:30]  # First 30 lines
                for line in diff_lines:
                    report.append(f"   {line}\n")
                
                if len(diff_content.split('\n')) > 30:
                    report.append("\n   [... truncated ...]\n")
                    report.append(f"   Full diff: git diff {self.branch1}..{self.branch2} -- {file_path}\n")
                
                report.append("\n")
        
        # Footer with actionable info
        report.append("\n" + "="*80 + "\n\n")
        report.append("RECOMMENDED ACTIONS\n")
        report.append("-" * 80 + "\n")
        
        if comparison_data['missing_in_branch2']:
            report.append(f"1. Review and merge {len(comparison_data['missing_in_branch2'])} missing file(s) from {self.branch1}\n")
        
        if comparison_data['modified_count']:
            report.append(f"2. Review code changes in {comparison_data['modified_count']} modified file(s)\n")
        
        if comparison_data['additional_in_branch2']:
            report.append(f"3. Evaluate {len(comparison_data['additional_in_branch2'])} new file(s) in {self.branch2}\n")
        
        report.append("\n")
        report.append("="*80 + "\n")
        report.append("Report generated by Branch Comparison Agent\n")
        
        return "".join(report)
    
    def generate_json_report(self, comparison_data: Dict) -> str:
        """Generate a JSON report with detailed information."""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "comparison": {
                "branch1": self.branch1,
                "branch2": self.branch2
            },
            "summary": {
                "total_files_branch1": comparison_data['total_files_branch1'],
                "total_files_branch2": comparison_data['total_files_branch2'],
                "common_files": comparison_data['common_files_count'],
                "missing_in_branch2": len(comparison_data['missing_in_branch2']),
                "additional_in_branch2": len(comparison_data['additional_in_branch2']),
                "modified_files": comparison_data['modified_count']
            },
            "details": {
                "missing_in_branch2": comparison_data['missing_in_branch2'],
                "additional_in_branch2": comparison_data['additional_in_branch2'],
                "modified_files": list(comparison_data['modified_files'].keys())
            }
        }
        return json.dumps(report_data, indent=2)
    
    def save_reports(self, comparison_data: Dict) -> Tuple[str, str]:
        """Save both Markdown and JSON reports."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Markdown Report
        md_report = self.generate_markdown_report(comparison_data)
        md_path = self.report_dir / f"comparison_report_{timestamp}.md"
        md_path.write_text(md_report)
        print(f"✓ Markdown report saved: {md_path}")
        
        # JSON Report
        json_report = self.generate_json_report(comparison_data)
        json_path = self.report_dir / f"comparison_report_{timestamp}.json"
        json_path.write_text(json_report)
        print(f"✓ JSON report saved: {json_path}")
        
        # Also save as latest
        (self.report_dir / "latest_comparison.md").write_text(md_report)
        (self.report_dir / "latest_comparison.json").write_text(json_report)
        
        return str(md_path), str(json_path)
    
    def run(self) -> Tuple[str, str]:
        """Run the complete comparison and generate reports."""
        print(f"Starting branch comparison in {self.repo_path}")
        comparison_data = self.compare_branches()
        md_report, json_report = self.save_reports(comparison_data)
        print(f"\n✓ Comparison complete!")
        return md_report, json_report


def main():
    """Main entry point."""
    import sys
    
    # Get repo path from command line or use current directory
    repo_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    branch1 = sys.argv[2] if len(sys.argv) > 2 else "master"
    branch2 = sys.argv[3] if len(sys.argv) > 3 else "QA"
    
    try:
        agent = BranchComparisonAgent(repo_path, branch1, branch2)
        md_report, json_report = agent.run()
        print(f"\nReports generated successfully!")
        print(f"Markdown: {md_report}")
        print(f"JSON: {json_report}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

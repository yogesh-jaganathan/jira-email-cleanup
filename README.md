# Jira Email Reference Cleanup Tool

A Python automation script to **search, back up, and optionally delete Jira issues**
that contain specific email addresses in the **summary, description, or comments**.

This tool is designed for **large-scale GDPR / data-cleanup operations** and supports
processing **20,000+ users safely** using Jira Cloud REST API v3.

---

## 🔧 Features

- 🔍 Searches **all Jira projects**
- 📧 Finds email references in:
  - Summary
  - Description
  - Comments
- 💾 Automatically creates a CSV backup before deletion
- 🧪 DRY-RUN mode (safe testing)
- 🚀 Fully automated bulk deletion (no confirmations)
- 📊 Handles large Excel input files

---

## 📁 Input Format

The script expects an Excel file: sample.xlsx



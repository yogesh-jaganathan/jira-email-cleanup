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

The script expects an Excel file (for example: `sample.xlsx`).

The Excel file must contain **at least one column**:

| email |
|------|
| user1@example.com |
| user2@example.com |

---

## ⚙️ Configuration

Update the following values in the script:

```python
JIRA_URL = "https://your-domain.atlassian.net"
USERNAME = "your-email@company.com"
API_TOKEN = "your_jira_api_token"
DRY_RUN = True  # Set to False to delete issues
🔐 Authentication (Recommended)
For security reasons, it is recommended to store the Jira API token
as an environment variable instead of hard-coding it.

Example (Linux / macOS)
bash
Copy code
export JIRA_API_TOKEN="your_jira_api_token"
Then update the script:

python
Copy code
import os
API_TOKEN = os.getenv("JIRA_API_TOKEN")
This prevents accidental exposure of credentials in version control.

▶️ How It Works
Reads email addresses from the Excel file

Searches Jira using the following JQL:

pgsql
Copy code
description ~ "email" OR comment ~ "email" OR summary ~ "email"
Collects all matching issues

Writes a CSV backup:

Copy code
backup_before_delete_file_1.csv
Deletes issues automatically (only if DRY_RUN = False)

🧪 DRY-RUN Mode (Recommended)
Default mode:

python
Copy code
DRY_RUN = True
No issues are deleted

Shows exactly what would be deleted

Always run this first before switching to live mode

⚠️ Disclaimer
This tool permanently deletes Jira issues when DRY_RUN is set to False.

Use this script at your own risk.
The author is not responsible for data loss caused by misuse or incorrect configuration.

📦 Installation
bash
Copy code
pip install -r requirements.txt
📜 requirements.txt
txt
Copy code
requests
pandas
tqdm
openpyxl

👤 Author
Yogesh Jaganathan
Product Support Engineer | Jira Automation | Python
GitHub: https://github.com/yogesh-jaganathan
LinkedIn: www.linkedin.com/in/yogesh-j-251a4739b

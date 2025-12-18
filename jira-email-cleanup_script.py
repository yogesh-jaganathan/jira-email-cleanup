import time
import requests
import pandas as pd
from tqdm import tqdm
from requests.auth import HTTPBasicAuth

# === Jira Configuration ===
JIRA_URL = "https://your-domain.atlassian.net"
USERNAME = "your-email@company.com"
API_TOKEN = "your_jira_api_token"  # <-- Replace with your valid Jira API token

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# === Global Mode Flag ===
DRY_RUN = True  # Set to False to actually delete tickets


# === Helper Functions ===

def search_issues_for_email(email):
    """
    Search ALL Jira issues (across all projects) where the given email is mentioned
    in the summary, description, or comments.
    Uses the new /rest/api/3/search/jql endpoint (POST).
    """
    all_issues = []
    start_at = 0
    jql = f'description ~ "{email}" OR comment ~ "{email}" OR summary ~ "{email}" OR "User\'s description[Paragraph]" ~ "{email}"'

    print(f"\n🔍 Searching Jira for mentions of: {email}")

    while True:
        payload = {
            "jql": jql,
            "maxResults": 100,
            "fields": ["id", "key", "summary", "issuetype"]
        }

        response = requests.post(
            f"{JIRA_URL}/rest/api/3/search/jql",
            headers=HEADERS,
            auth=HTTPBasicAuth(USERNAME, API_TOKEN),
            json=payload
        )

        if response.status_code == 410:
            print(f"⚠️ Jira API 410 (Gone): The old API has been retired. "
                  f"Check your Jira plan or API permissions.")
            break
        elif response.status_code != 200:
            print(f"❌ Error fetching issues for {email}: {response.status_code} {response.text}")
            break

        data = response.json()
        issues = data.get("issues", [])
        if not issues:
            break

        all_issues.extend(issues)

        if len(issues) < 100:
            break

        start_at += len(issues)
        time.sleep(0.5)

    print(f"✅ Found {len(all_issues)} issues mentioning {email}")
    return all_issues


def write_output(data, file_name, head):
    """
    Write collected issue data to a CSV file.
    """
    output_file = f"{file_name}.csv"
    pd.DataFrame(data).to_csv(output_file, mode='a', index=False, header=head)
    print(f"💾 Issues saved to {output_file}")


def delete_issue(issue_key):
    """
    Delete a Jira issue by key.
    """
    if DRY_RUN:
        print(f"🧪 [DRY-RUN] Would delete issue: {issue_key}")
        return

    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    response = requests.delete(url, headers=HEADERS, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    if response.status_code == 204:
        print(f"🗑️ Deleted: {issue_key}")
    else:
        print(f"❌ Failed to delete {issue_key}: {response.status_code} {response.text}")

    time.sleep(0.5)


# === FIXED bulk_delete() ===
def bulk_delete(issues):
    """
    Bulk delete issues without asking per-ticket confirmation.
    """
    if not issues:
        print("ℹ️ No issues to delete.")
        return

    print(f"⚠️ You are about to delete {len(issues)} issues.")

    if DRY_RUN:
        print("🧪 DRY-RUN mode — no actual deletions will occur.")
        return

    # --- No confirmation needed, fully automatic ---
    print("🚀 Proceeding with automatic bulk deletion...")

    for issue in tqdm(issues, desc="Deleting issues in bulk"):
        delete_issue(issue["Issue Key"])


# === Main Execution ===
if __name__ == "__main__":
    file_path = "sample_file.xlsx"  # Update with your Excel file
    sheet_name = "Sheet1"

    df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

    df.columns = df.columns.str.strip().str.lower()

    need_header = True

    print("🚦 Mode:", "DRY-RUN (no deletions will happen)" if DRY_RUN else "LIVE MODE (issues will be deleted!)")

    for _, row in df.iterrows():
        if "email" not in row or pd.isna(row["email"]):
            continue

        email = str(row["email"]).strip()
        if not email:
            continue

        print(f"\n=== Processing user: {email} ===")

        issues_data = search_issues_for_email(email)

        issues = []
        for issue in issues_data:
            fields = issue.get("fields", {})
            issues.append({
                "Email": email,
                "Issue Key": issue["key"],
                "Summary": fields.get("summary", ""),
                "Issue Type": fields.get("issuetype", {}).get("name", ""),
                "URL": f"{JIRA_URL}/browse/{issue['key']}"
            })

        if issues:
            write_output(issues, "backup_before_delete_file_1", need_header)
            need_header = False

            if not DRY_RUN:
                bulk_delete(issues)
            else:
                print("🧪 DRY-RUN: Skipped deletion (backup only).")
        else:
            print(f"ℹ️ No issues found mentioning {email}.")

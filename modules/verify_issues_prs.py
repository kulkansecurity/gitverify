from datetime import datetime
from include import gh_api

def run(repository, contributors, output_obj):
    c_logins = [item['login'] for item in contributors]
    issues_prs = gh_api.fetch_issues_and_prs(repository)
    not_created_by_contributors = 0
    i_pr_len = len(issues_prs)
    print(f"Running verifications on {i_pr_len} repository issues and PRs..")
    for i in issues_prs:
        if i.get('user').get('login') not in c_logins:
            not_created_by_contributors += 1

    if i_pr_len:
        if not_created_by_contributors > 0:
            output_obj.positive(f"Sum of issues and PRs NOT created by contributors: {not_created_by_contributors}", 0.5)
        else:
            output_obj.negative(f"All {i_pr_len} existing issues and PRs were created by contributors.", 0.75)
    else:
        output_obj.negative(f"The repository has no record of Issues or Pull Requests.", 0.5)

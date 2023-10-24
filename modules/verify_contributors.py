from datetime import datetime
from include import gh_api

def run(repository, output_obj):
    contributors = gh_api.fetch_contributors(repository)
    c_len = len(contributors)
    print("Running verifications on {} contributors..".format(c_len))
    for c in contributors:
        contributor = gh_api.fetch_contributor(c)

        days = (datetime.now() - datetime.strptime(contributor.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")).days
        if days < 365:
            output_obj.negative(f"Contributor [{contributor['html_url']}] is only {days} days old.", 0.5)
        else:
            years = "{:.2f}".format(days / 365)
            output_obj.positive(f"Contributor [{contributor['html_url']}] is {years} years old.", 0.5)

        public_repos = int(contributor.get('public_repos'))
        if public_repos > 1:
            output_obj.positive(f"Contributor [{contributor['html_url']}] has {public_repos} total public repos.")

        followers = contributor.get('followers')
        if followers <= len(contributors):
            output_obj.negative(f"Contributor [{contributor['html_url']}] has less or equal followers than total repo contributors.", 0.5)
    return contributors

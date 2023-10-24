from datetime import datetime
from include import gh_api

def run(repository, output_obj):
    print("Running verifications on repository metadata..")
    if repository.get('private') == True:
        output_obj.debug("Repository is set to private.")

    days = (datetime.now() - datetime.strptime(repository.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")).days
    if days < 365:
        output_obj.negative(f"Repository [{repository['html_url']}] is only {days} days old.", 0.5)
    else:
        years = "{:.2f}".format(days / 365)
        output_obj.positive(f"Repository [{repository['html_url']}] is {years} years old.", 0.5)

    if repository.get('archived') == True:
        output_obj.negative(f"Repository is archived and therefore likely no longer maintained.", 1)

    if repository.get('disabled') == True:
        output_obj.negative(f"Repository is disabled and therefore likely no longer maintained.", 1)

    if repository.get('organization'):
        org_url = repository.get('organization').get('url')
        output_obj.positive(f"Repository is owned by an Organization {org_url} - (Note that Creating an Org is free in github.com.)", 0.1)

    # Let's use the amount of contributors as threshold for several checks
    THRESHOLD = len(gh_api.fetch_contributors(repository))

    subscribers = int(repository.get('subscribers_count'))
    if subscribers <= THRESHOLD:
        output_obj.negative(f"Subscribers count ({subscribers}) is lower or equal to contributors count ({THRESHOLD}).", 0.5)

    stars = int(repository.get('stargazers_count'))
    if stars < THRESHOLD:
        output_obj.negative(f"Stars count ({stars}) is lower or equal to contributors count ({THRESHOLD}).", 0.5)

    watchers = int(repository.get('watchers_count'))
    if watchers < THRESHOLD:
        output_obj.negative(f"Watchers count ({watchers}) is lower or equal to contributors count ({THRESHOLD}).", 0.5)
    

# GitVerify

GitVerify is a tool designed to analyze GitHub repositories and provide insights into their trustworthiness. It gathers data from the GitHub API and, optionally, performs VirusTotal checks on associated domains, then presents the results in a concise manner. Supported output formats include: text, json, csv.

<p align="center">
  <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/148867002/277650292-91a21f8e-a366-4786-a534-8b4cf8842b0b.png" alt="gitverify"/>
</p>


## Disclaimer

- The Criteria verified by GitVerify is constant Work-in-Progress.
- Domain extraction is performed via Github's Code API search and is not perfect as it won't catch every single possible domain reference/format.

## Key Features:

- **Metadata Verification** (modules/verify_metadata.py):
  - Analyzes the age of the repository. If the repository is too new then it could likely be a replica or copy of the repository you or your team intends to use.
  - It also checks if the repository is archived or disabled. Cloning and using an archived/disabled repository may lead to using old/vulnerable/deprecated code.
  - It checks if the repository is owned by a person or an organization. Creating organizations is pretty straightforward, hence org-owned repositories aren’t necessarily a signal of reliability.
  - Checks the number of subscribers, stars, and watchers against the amount of repository contributors. This can later be improved to check if the subscribers, stars, and watchers are exactly the same identities as the contributors instead of merely relying on numbers.

- **Contributors Verification** (modules/verify_contributors.py):
  - Checks if the contributor has other public repositories than the one being verified. Lack of other repositories isn’t a bad thing, but it certainly gives you more context.
  - Examines the account creation time of contributors. A recently created account might be less reliable than a contributor with a longer history in GitHub.
  - It also checks the amount of followers each of the contributors have. We’re considering you might use gitverify for potentially reliable projects, therefore the idea being you’re going to spot fake or incorrect repositories before you use them.

- **Issues and PRs Verification** (modules/verify_issues_prs.py):
  - Scans through issues and pull requests to validate if they were only created by contributors. To the human eye, a project with Issues and Pull Requests might seem more reliable than one which has none; which is why we’re trying to catch potential ‘fake activity’ this way.

- **Domain Verification** (modules/verify_domains.py):
  - Extracts using GitHub’s Code API a list of domains and (optionally) scans them using the VirusTotal API to detect any flagged by the community as dangerous. The extraction logic is quite simple and can be further enhanced.

## Important: Environment Variables Configuration

Before using the tool, it's **strongly recommended** to set up the following environment variables:

- **GH_ACCESS_TOKEN**: By setting up your GitHub API token as an environment variable, you'll bypass the strict rate limits for unauthenticated requests. You can create your token [here](https://github.com/settings/tokens).
- **VT_API_KEY**: If you wish to utilize the VirusTotal check feature, ensure to set up your VirusTotal API key as an environment variable. Obtain your API key from the [VirusTotal website](https://www.virustotal.com/).

Without these configurations, the functionality of GitVerify may be limited.

## Usage:

To get started with GitVerify, you can run the script as follows:

### Checking a Single Repository:

```
./gitverify.py -r https://github.com/user/repository
```

### Checking Multiple Repositories:

If you have a file (`repos.txt`) with multiple repositories listed line-by-line:

```
https://github.com/user/repo1
https://github.com/user/repo2
```

Run:

```
./gitverify.py -rf repos.txt
```

### Additional Options:

- **Specify Output File**: `-o output.txt`
- **Set Output Format**: `-f json` (supports `text`, `json`, or `csv`)
- **Disable VirusTotal Checks**: `-disable-vt`
- **Verbose Mode (additional details)**: `-v or --verbose`


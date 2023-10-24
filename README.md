# GitVerify

GitVerify is a tool designed to analyze GitHub repositories and provide insights into their trustworthiness. It gathers data from the GitHub API and, optionally, performs VirusTotal checks on associated domains, then presents the results in a concise manner. Supported output formats include: text, json, csv.

<p align="center">
  <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/148867002/277650292-91a21f8e-a366-4786-a534-8b4cf8842b0b.png" alt="gitverify"/>
</p>


## Disclaimer

- The Criteria verified by GitVerify is constant Work-in-Progress.
- Domain extraction is performed via Github's Code API search and is not perfect as it won't catch every single possible domain reference/format.

## Key Features:

- **Metadata Verification**: Verifies age of the repository; whether it is archived or disabled, subscribers, stars and watchers count, among other items.
- **Contributors Verification**: Analyzes contributors to the repository, checking account creation time, count of followers, additional repositories, and more.
- **Issues and PRs Verification**: Scans through issues and pull requests to verify if they were only created by contributors, and potentially more checks in the future.
- **Domain Verification (with VirusTotal)**: Optionally performs a scan on domains associated with the repository using the VirusTotal API to ensure they aren't flagged as malicious.

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


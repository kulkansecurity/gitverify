#!/usr/bin/env python3
import os, sys
from include import gh_api, output, arg_parser
from modules import verify_metadata
from modules import verify_contributors
from modules import verify_domains
from modules import verify_issues_prs


if __name__ == "__main__":
    args = arg_parser.parse_arguments()
    output_obj = output.Output(verbose=args.verbose, outfile=args.outfile, outformat=args.format)

    print("""
░██████╗░██╗████████╗██╗░░░██╗███████╗██████╗░██╗███████╗██╗░░░██╗
██╔════╝░██║╚══██╔══╝██║░░░██║██╔════╝██╔══██╗██║██╔════╝╚██╗░██╔╝
██║░░██╗░██║░░░██║░░░╚██╗░██╔╝█████╗░░██████╔╝██║█████╗░░░╚████╔╝░
██║░░╚██╗██║░░░██║░░░░╚████╔╝░██╔══╝░░██╔══██╗██║██╔══╝░░░░╚██╔╝░░
╚██████╔╝██║░░░██║░░░░░╚██╔╝░░███████╗██║░░██║██║██║░░░░░░░░██║░░░
░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░
GitVerify: Is the repo trustworthy? Make an informed decision.
v1.0 - https://www.kulkan.com
######################################################################################""")

    # Let's warn the user that unauth RateLimits are pretty low
    if os.environ.get("GH_ACCESS_TOKEN", None) == None:
        output_obj.warn("GH_ACCESS_TOKEN environment variable not set, using GitHub RateLimits for anonymous queries")
        output_obj.warn("Unauthenticated requests to the Github API will enforce a very low and strict RateLimit")
        print("For information on how to create a GitHub API Access Token refer to: ")
        print("https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens")

    if os.environ.get("VT_API_KEY", None) == None:
        output_obj.warn("VT_API_KEY environment variable not set, disabling VirusTotal checks.")
        print("For information on how to create a VirusTotal API Key refer to: ")
        print("https://www.virustotal.com/en/documentation/public-api/")
        args.disable_vt = True

    if not args.repositories_file:
        args.repositories_file = [args.repository]

    for repo in args.repositories_file:
        try:
            repository = gh_api.fetch_repository(repo)
            print("######################################################################################")
            print("Now verifying repository: {}".format(repository.get('full_name')))
        except Exception as ex:
            print("Unable to pull data for the repository that was provided. Is it a valid repo URL?")
            if args.verbose:
                print(ex)
            sys.exit()

        output_obj.initialize_repo_output(repository.get('full_name'))
        verify_metadata.run(repository, output_obj)
        # We store the result from contributors() to prevent calling it again for I+PRS
        contributors = verify_contributors.run(repository, output_obj)
        verify_issues_prs.run(repository, contributors, output_obj)

        if not args.disable_vt:
            verify_domains.run(repository, output_obj)


    output_obj.doOutput()
    sys.exit()


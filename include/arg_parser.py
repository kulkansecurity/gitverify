import os, sys, argparse

def parse_repositories_from_file(filepath):
    if not os.path.exists(filepath):
        raise argparse.ArgumentTypeError(f"File not found: {filepath}")

    with open(filepath, 'r') as f:
        repositories = f.read().splitlines()

    for repo in repositories:
        validate_repository(repo)

    print("Loaded {} repositories.".format(len(repositories)))
    return repositories

def validate_repository(repo):
    if not repo.startswith("https://"):
        raise argparse.ArgumentTypeError(f"Invalid repository URL '{repo}'. It should start with 'https://'.")
    return repo


def parse_arguments():
    parser = argparse.ArgumentParser(description="GitVerify")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-r', '--repository',
            type=validate_repository,
            action='store',
            help='The repository to check.')

    group.add_argument('-rf', '--repositories-file',
            type=parse_repositories_from_file,
            action='store',
            help='A file containing repositories separated by newlines.')

    parser.add_argument('--disable-vt', action='store_true', help='Disable VirusTotal checks on domains.')

    parser.add_argument('-v', '--verbose', 
            action='store_true', 
            default=False, 
            help='Enable extra verbosity (Debug, Dev-narcisism).')

    parser.add_argument('-o', '--outfile', 
            type=str, 
            action='store',
            help='Set the location for the output log file.')

    parser.add_argument('-f', '--format', type=str, action='store',
            default='text',
            help='Format for log file (text,json,csv) - default: text',
            choices = ['text', 'json', 'csv'])

    args = parser.parse_args()

    if args.outfile:
        if os.path.isdir(args.outfile):
            print("[!] Can't specify a directory as the output file, exiting.")
            sys.exit()
        if os.path.isfile(args.outfile):
            target = args.outfile
        else:
            target = os.path.dirname(args.outfile)
            if target == '':
                target = '.'

        if not os.access(target, os.W_OK):
            print("[!] Cannot write to output file, exiting")
            sys.exit()

    return args

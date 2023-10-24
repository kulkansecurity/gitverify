from datetime import datetime
from include import gh_api, vt_api

def run(repository, output_obj):
    print("Extracting domains from repository code and validating with VirusTotal..")
    domains = gh_api.fetch_domains_from_code(repository.get('full_name'))
    try:
        for domain in domains:
            if domain in ["localhost","127.0.0.1"]:
                continue
            stats = vt_api.domain_report(domain)["data"]["attributes"]["last_analysis_stats"]
            if int(stats["malicious"]) > 1:
                output_obj.negative(f"Domain {domain} extracted from code considered malicious by VirusTotal. The results are: " + str(stats), 0.5)

            if int(stats["malicious"]) > int(stats["harmless"]):
                output_obj.negative(f"Domain {domain} has more malicious than harmless reviews by VirusTotal. The results are: " + str(stats), 1)
    except Exception as ex:
        output_obj.debug(ex)




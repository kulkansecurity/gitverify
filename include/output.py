import json, csv, os
from io import StringIO

class Output:
    ANSI_RESET = "\033[0m"
    ANSI_BLUE = "\033[94m"
    ANSI_GREEN = "\033[92m"
    ANSI_RED = "\033[91m"
    ANSI_YELLOW = "\033[93m"


    def __init__(self, verbose=False, outfile=None, outformat='text'):
        self._verbose = verbose
        self._outfile = None
        if outfile:
            self._outfile = open(outfile, 'a+')

        self._outformat = outformat
        self._repositories = {}
        self._index = None

    def initialize_repo_output(self, repository):
        if repository not in self._repositories:
            self._repositories[repository] = {}
            self._repositories[repository]["messages"] = {"positive": [], "negative": []}
            self._repositories[repository]["scoring"] = {"positive_score": 0.0, "negative_score": 0.0}
            
        self._index = repository

    def positive(self, message, weight=0):
        colored_message = f"{self.ANSI_GREEN}[Like]{self.ANSI_RESET} {message}"
        self._repositories[self._index]["messages"]["positive"].append(colored_message)
        self._repositories[self._index]["scoring"]["positive_score"] += weight

    def negative(self, message, weight=0):
        colored_message = f"{self.ANSI_RED}[Dislike]{self.ANSI_RESET} {message}"
        self._repositories[self._index]["messages"]["negative"].append(colored_message)
        self._repositories[self._index]["scoring"]["negative_score"] += weight

    def debug(self, message):
        if self._verbose:
            colored_message = f"{self.ANSI_YELLOW}[D]{self.ANSI_RESET} {message}"
            return print(colored_message)

    def warn(self, message):
        colored_message = f"{self.ANSI_YELLOW}{message}{self.ANSI_RESET}"
        return print(colored_message)

    def _create_text_output(self):
        output = ""
        for repo, data in self._repositories.items():
            output += f"Printing results for repository {repo}..\n"
            output += "\n".join(data["messages"]["positive"])
            output += "\n" + "\n".join(data["messages"]["negative"])
            output += "\n" + f"{self.ANSI_GREEN}Total positive score:{self.ANSI_RESET} {data['scoring']['positive_score']}"
            output += "\n" + f"{self.ANSI_RED}Total negative score:{self.ANSI_RESET} {data['scoring']['negative_score']}\n\n"
        return output

    def _create_json_output(self):
        output_data = []
        for repo, data in self._repositories.items():
            output_data.append({ "repository": repo, "criteria": data["messages"], "scoring": data["scoring"] })
        return json.dumps(output_data, indent=4)

    def _create_csv_output(self):
        output = StringIO()
        writer = csv.writer(output)
        for repo, data in self._repositories.items():
            for msg_type, msgs in data["messages"].items():
                for msg in msgs:
                    writer.writerow([repo, msg_type, msg])
            for msg_type, score in data["scoring"].items():
                writer.writerow([repo, msg_type, score])
        return output.getvalue()

    def doOutput(self):
        if self._outformat == 'text':
            output = self._create_text_output()
        elif self._outformat == 'json':
            output = self._create_json_output()
        elif self._outformat == 'csv':
            output = self._create_csv_output()
        else:
            raise ValueError("Unsupported format!")

        if self._outfile:
            print(f"Writing output to {self._outfile.name} in format {self._outformat}")
            if self._outformat == 'csv' and os.path.getsize(self._outfile.name) == 0:
                writer = csv.writer(self._outfile)
                writer.writerow(["Repository", "Item", "Value"])
            self._outfile.write(output)
            self._outfile.write("\n")
        else:
            print(output)


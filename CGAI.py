import os
import datetime
import webbrowser
import subprocess

class CyberGeniusAI:
    def __init__(self):
        self.case_id = 1
        self.case_folder = "case_files"
        self.initialize_case_folder()

    def initialize_case_folder(self):
        if not os.path.exists(self.case_folder):
            os.mkdir(self.case_folder)

    def create_case_file(self, subject):
        filename = f"case_{self.case_id}_{subject}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.case_folder, filename)
        with open(filepath, "w") as f:
            f.write(f"Case ID: {self.case_id}\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Date and Time: {datetime.datetime.now()}\n\n")
        self.case_id += 1
        return filepath

    def perform_shodan_search(self, subject):
        shodan_api_key = "YOUR_SHODAN_API_KEY"
        shodan_command = f"shodan search --key {shodan_api_key} {subject}"
        try:
            shodan_results = subprocess.run(shodan_command, shell=True, capture_output=True, text=True)
            return shodan_results.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing Shodan search: {e}\n"

    def perform_theharvester(self, subject):
        theharvester_command = f"theharvester -d {subject} -b google -l 500 -f {os.path.join(self.case_folder, 'emails.txt')}"
        try:
            subprocess.run(theharvester_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing TheHarvester: {e}")

    def perform_recon_ng(self, subject):
        recon_ng_command = f"recon-ng -m recon/domains-hosts/threatcrowd_api -c 'set source {subject}' -x"
        try:
            subprocess.run(recon_ng_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing Recon-ng: {e}")

    def perform_osint(self):
        subject = input("Enter the subject for OSINT: ")
        case_file = self.create_case_file(subject)

        shodan_results = self.perform_shodan_search(subject)
        with open(case_file, "a") as f:
            f.write("Shodan Results:\n")
            f.write(shodan_results + "\n\n")

        self.perform_theharvester(subject)
        self.perform_recon_ng(subject)

        # Open browser for informative search
        search_url = f"https://www.google.com/search?q={subject}"
        webbrowser.open(search_url)

        print(f"OSINT completed. Case file created: {case_file}")

    def run(self):
        print("Welcome to CyberGeniusAI - OSINT Edition!")
        while True:
            print("\nMenu:")
            print("1. Perform OSINT")
            print("0. Exit")
            choice = input("Select an option: ")
            if choice == "1":
                self.perform_osint()
            elif choice == "0":
                print("Exiting CyberGeniusAI - OSINT Edition.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    cyber_genius = CyberGeniusAI()
    cyber_genius.run()

import cloudscraper
import sys
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style

# Create a scraper instance which will act like our session
scraper = cloudscraper.create_scraper()

def from_wordlist(domain, wordlist_file, context, output_file=None):
    """
    Discovers API endpoints from a given wordlist.
    """
    print("[*] Starting wordlist-based discovery...")
    found_endpoints = []
    timeout = context.get('timeout', 20) # Get timeout from context, default to 20

    try:
        with open(wordlist_file, 'r') as f:
            endpoints = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Error: Wordlist file not found at '{wordlist_file}'{Style.RESET_ALL}")
        sys.exit(1)

    if not domain.startswith('http'):
        target_domain = 'https://' + domain
    else:
        target_domain = domain

    for endpoint in endpoints:
        full_url = urljoin(target_domain, endpoint)
        try:
            response = scraper.get(full_url, timeout=timeout)
            if response.status_code != 404:
                print(f"{Fore.GREEN}[+] Found: {full_url} (Status: {response.status_code}){Style.RESET_ALL}")
                found_endpoints.append(f"{full_url} (Status: {response.status_code})")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Connection to {full_url} failed: {e}{Style.RESET_ALL}")
            pass

    print("[+] Wordlist discovery finished.")
    if output_file and found_endpoints:
        with open(output_file, 'w') as f:
            for item in found_endpoints:
                f.write(item + "\n")
        print(f"[+] Wordlist results saved to {output_file}")
    return found_endpoints

def from_js_files(domain, context, output_file=None):
    """
    Discovers API endpoints by scanning linked JavaScript files.
    """
    print("[*] Starting JavaScript file analysis...")
    found_endpoints = []
    timeout = context.get('timeout', 20) # Get timeout from context

    if not domain.startswith('http'):
        target_domain = 'https://' + domain
    else:
        target_domain = domain
    try:
        response = scraper.get(target_domain, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', src=True)
        path_pattern = re.compile(r'[\'"](/[^/].*?)[\'"]')

        for tag in script_tags:
            script_url = urljoin(target_domain, tag['src'])
            try:
                script_response = scraper.get(script_url, timeout=timeout)
                potential_paths = path_pattern.findall(script_response.text)
                for path in potential_paths:
                    # Filter for common API keywords to reduce noise
                    if 'api' in path or 'v1' in path or 'v2' in path or 'graphql' in path:
                        if path not in found_endpoints:
                            print(f"{Fore.GREEN}[+] Found in JS: {path}{Style.RESET_ALL} (from {script_url})")
                            found_endpoints.append(path)
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Could not fetch JS file: {script_url} | Reason: {e}{Style.RESET_ALL}")
                continue
    except Exception as e:
        print(f"{Fore.RED}[-] Critical Error fetching main page: {e}{Style.RESET_ALL}")

    print("[+] JavaScript analysis finished.")
    if output_file and found_endpoints:
        unique_paths_to_save = sorted(list(set(found_endpoints)))
        with open(output_file, 'a') as f:
            f.write("\n--- JS Analysis Results ---\n")
            for item in unique_paths_to_save:
                f.write(item + "\n")
        print(f"[+] JS analysis results appended to {output_file}")

    return list(set(found_endpoints))

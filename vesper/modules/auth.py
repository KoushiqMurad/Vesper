# vesper/modules/auth.py
import cloudscraper
from urllib.parse import urljoin
from colorama import Fore, Style

scraper = cloudscraper.create_scraper()

def check_unauthenticated_access(base_url, endpoints, context):
    """
    Checks a list of endpoints for unauthenticated access vulnerabilities.
    """
    print("\n[*] Starting unauthenticated access scan...")
    vulnerable_endpoints = []
    timeout = context.get('timeout', 20)

    for endpoint in endpoints:
        full_url = urljoin(base_url, endpoint)
        try:
            response = scraper.get(full_url, timeout=timeout)
            
            # Check for success codes (2xx) which indicate access
            if 200 <= response.status_code < 300:
                print(f"{Fore.RED}[!!!] Potential Unauthenticated Access: {full_url} (Status: {response.status_code}){Style.RESET_ALL}")
                vulnerable_endpoints.append(f"{full_url} (Status: {response.status_code})")
            else:
                # This is just for verbose feedback, can be removed for a quieter tool
                print(f"{Fore.GREEN}[+] Endpoint is protected: {full_url} (Status: {response.status_code}){Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error checking {full_url}: {e}{Style.RESET_ALL}")
            continue
            
    if not vulnerable_endpoints:
        print("[+] No unauthenticated endpoints found.")
    
    print("[+] Authentication scan finished.")
    return vulnerable_endpoints

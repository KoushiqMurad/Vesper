import argparse
from vesper.modules import discover, auth, jwt_attacker
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def display_banner():
    """Displays the final, clear text banner."""
    title = "V  E  S  P  E  R"
    subtitle = "An API Security Recon & Exploitation Toolkit"
    author = "by Koushiq Murad"
    
    print(Fore.CYAN + "=" * 60)
    print(f"{Style.BRIGHT}{title.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{subtitle.center(60)}")
    print(f"{Fore.RED}{author.center(60)}")
    print(Fore.CYAN + "=" * 60)
    print() # Add a newline for spacing

def main():
    parser = argparse.ArgumentParser(description="Vesper - An API Security Recon & Exploitation Toolkit.")
    
    # Reconnaissance Arguments
    recon_group = parser.add_argument_group('Reconnaissance')
    recon_group.add_argument("-d", "--domain", help="The target domain to scan (e.g., example.com)")
    recon_group.add_argument("-w", "--wordlist", help="Path to a wordlist file.")
    recon_group.add_argument("--js", help="Enable JavaScript file analysis.", action="store_true")
    recon_group.add_argument("--auth", help="Run unauthenticated access check.", action="store_true")

    # JWT Operations Arguments
    jwt_group = parser.add_argument_group('JWT Operations')
    jwt_group.add_argument("-t", "--token", help="The JWT to analyze or attack.")
    jwt_group.add_argument("--jwt-decode", help="Decode the provided JWT.", action="store_true")
    jwt_group.add_argument("--jwt-alg-none", help="Perform the 'alg=none' signature bypass attack.", action="store_true")
    jwt_group.add_argument("--jwt-bruteforce", help="Brute-force the HS256 secret key. Requires -w.", action="store_true")
    jwt_group.add_argument("--jwt-sign", help="Forge a new HS256 token. Requires --payload and --secret.", action="store_true")
    jwt_group.add_argument("--payload", help="The JSON payload to encode in the new token (e.g., '{\"admin\":true}')")
    jwt_group.add_argument("--secret", help="The secret key to sign the new token with.")
    
    # General Arguments
    parser.add_argument("-o", "--output", help="File to save the output results.")
    parser.add_argument("--timeout", help="Set the timeout for web requests.", type=int, default=20)

    args = parser.parse_args()
    display_banner()

    # --- JWT LOGIC ---
    if args.jwt_sign:
        if not (args.payload and args.secret):
            print(f"{Fore.RED}[-] Error: Forging a token requires both --payload and --secret arguments.{Style.RESET_ALL}")
        else:
            jwt_attacker.sign_hs256_token(args.payload, args.secret)
        return

    if args.token:
        if args.jwt_decode:
            jwt_attacker.decode_token(args.token)
        if args.jwt_alg_none:
            jwt_attacker.attack_alg_none(args.token)
        if args.jwt_bruteforce:
            if not args.wordlist:
                print(f"{Fore.RED}[-] Error: The JWT brute-force attack requires a wordlist. Use the -w flag.{Style.RESET_ALL}")
            else:
                jwt_attacker.attack_hs256_bruteforce(args.token, args.wordlist)
        return

    # --- RECON LOGIC ---
    if not args.domain:
        print(f"{Fore.YELLOW}[-] No target domain specified for recon. Use -d <domain> or provide JWT arguments.{Style.RESET_ALL}")
        return

    print(f"[*] Vesper Initializing Scan on: {Style.BRIGHT}{args.domain}{Style.RESET_ALL}")
    print("==================================================")
    
    found_endpoints = []
    context = {'timeout': args.timeout}
    base_url = f"https://{args.domain}" if not args.domain.startswith('http') else args.domain

    if args.wordlist and (args.js or args.auth):
         wordlist_results = discover.from_wordlist(args.domain, args.wordlist, context, args.output)
         for result in wordlist_results:
             path = result.split(" (Status:")[0].replace(base_url, "")
             found_endpoints.append(path)

    if args.js:
        js_results = discover.from_js_files(args.domain, context, args.output)
        found_endpoints.extend(js_results)

    unique_endpoints = sorted(list(set(found_endpoints)))

    if args.auth and unique_endpoints:
        auth.check_unauthenticated_access(base_url, unique_endpoints, context)
    elif args.auth:
        print(f"{Fore.YELLOW}[-] Auth check skipped: No endpoints were discovered to test.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

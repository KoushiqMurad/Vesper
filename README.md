<div align="center">

```

# \============================================================ V  E  S  P  E  R An API Security Recon & Exploitation Toolkit by Koushiq Murad

````
</div>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" alt="Python Version">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
    <img src="https://img.shields.io/badge/Status-Active_Development-orange?style=for-the-badge" alt="Project Status">
</p>

Vesper is a lightweight, powerful toolkit designed for the modern security researcher focused on API penetration testing. It automates the tedious parts of reconnaissance and includes a dedicated suite for finding and exploiting common JWT vulnerabilities, allowing you to focus on what matters: finding critical flaws.

---

## ✨ Features

Vesper's capabilities are organized into two main categories: Reconnaissance and JWT Attacks.

#### Reconnaissance
-   **Endpoint Discovery (Wordlist):** Brute-force common API endpoint paths from a provided wordlist.
-   **Endpoint Discovery (JavaScript Analysis):** Intelligently parse linked JavaScript files on a target to discover hidden or undocumented API paths.
-   **Unauthenticated Access Scanning:** Automatically test a list of discovered endpoints to find sensitive functionality exposed without authentication.

#### JWT (JSON Web Token) Operations
-   **Token Decoder:** Quickly parse any JWT to clearly view its header and payload.
-   **`alg=none` Attack:** Automatically generate a malicious token with the signature stripped, testing for the classic signature bypass vulnerability.
-   **HS256 Secret Key Brute-Forcer:** A multi-threaded cracker to rapidly guess weak HS256 secret keys from a wordlist.
-   **HS256 Token Forger:** Create and sign your own custom JWTs with any payload and secret key for advanced testing.

---

## 🚀 Installation

Vesper is designed to be simple to set up.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/KoushiqMurad/vesper.git](https://github.com/KoushiqMurad/vesper.git)
    cd vesper
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🛠️ Usage Guide

Vesper is controlled via command-line arguments. Below are examples for every feature.

### **Reconnaissance**

> **Note:** All recon commands require the `-d` or `--domain` flag.

-   **Discover endpoints using a wordlist:**
    ```bash
    python main.py -d example.com -w wordlist.txt
    ```

-   **Discover endpoints by analyzing JavaScript files:**
    ```bash
    python main.py -d example.com --js
    ```

-   **Discover endpoints and then check them for unauthenticated access:**
    ```bash
    python main.py -d example.com --js --auth
    ```

-   **Save all output to a file:**
    ```bash
    python main.py -d example.com --js --auth -o results.txt
    ```

### **JWT Operations**

> **Note:** All JWT commands require the `-t` or `--token` flag, or the `--jwt-sign` flag.

-   **Decode a JWT to view its contents:**
    ```bash
    python main.py -t "eyJhbGciOi..." --jwt-decode
    ```

-   **Perform the `alg=none` signature bypass attack:**
    ```bash
    python main.py -t "eyJhbGciOi..." --jwt-alg-none
    ```

-   **Brute-force an HS256 secret key using a wordlist:**
    ```bash
    python main.py -t "eyJhbGciOi..." --jwt-bruteforce -w passwords.txt
    ```

-   **Forge a new HS256 token with a custom payload and secret:**
    ```bash
    python main.py --jwt-sign --payload '{"admin":true,"user":"koushiq"}' --secret 'supersecret123'
    ```

---

## ⚠️ Disclaimer

Vesper is intended for educational purposes and authorized security testing only. Do not use this tool on any system you do not have explicit permission to test. The author is not responsible for any misuse or damage caused by this tool.
````

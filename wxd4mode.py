import requests
from colorama import Fore, Style, init
import os
import time

# Inisialisasi colorama
init()

# File yang berisi daftar proxy
proxy_file = "active_proxies.txt"

# File untuk menyimpan proxy yang aktif
output_file = "active_proxies.txt"

# URL yang akan diakses untuk menguji proxy
test_url = "http://checkip.amazonaws.com"  # Ganti dengan URL yang lebih ringan jika perlu

# URL untuk mendapatkan daftar proxy dari API
proxy_api_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

# Mybanner
banner = """

=========================================================================

 ##   ##   ####    #####     #####   #####     #####   ##  ##   #####   
 ##   ##    ##      ## ##   ##   ##   ## ##   ##   ##  ##  ##    ## ##  
 ##   ##    ##      ##  ##  ##   ##   ##  ##  ##   ##   ####     ##  ## 
 ## # ##    ##      ##  ##  ##   ##   ##  ##  ##   ##    ##      ##  ## 
 #######    ##      ##  ##  ##   ##   ##  ##  ##   ##   ####     ##  ## 
 ### ###    ##      ## ##   ##   ##   ## ##   ##   ##  ##  ##    ## ##  
 ##   ##   ####    #####     #####   #####     #####   ##  ##   #####   
                                                                        
=========================================================================
Fb : widodo.151
Pandan.Ngraho.Bjngoro
=========================================================================
"""
#####################################################################################

# Fungsi untuk membersihkan terminal
def clear_terminal():
    # Periksa sistem operasi dan jalankan perintah yang sesuai
    if os.name == 'nt':  # Untuk Windows
        os.system('cls')
    else:  # Untuk macOS dan Linux
        os.system('clear')


# Fungsi untuk membaca daftar proxy dari file
def read_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.read().splitlines()
    return proxies

# Fungsi untuk mendapatkan daftar proxy dari API
def fetch_proxies_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        proxies = response.text.splitlines()
        return proxies
    else:
        print(Fore.RED + "Failed to fetch proxies from API" + Style.RESET_ALL)
        return []

# Fungsi untuk menguji proxy
def test_proxy(proxy, proxy_type):
    try:
        proxies = {}
        if proxy_type == "http":
            proxies = {"http": proxy, "https": proxy}
        elif proxy_type == "socks4":
            proxies = {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
        elif proxy_type == "socks5":
            proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}

        response = requests.get(test_url, proxies=proxies, timeout=1)  # Timeout lebih pendek
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException as e: # Tangani exception request
        #print(f"Error testing {proxy}: {e}") #Print error untuk debugging
        pass
    return False

# Fungsi untuk menyimpan proxy yang aktif ke dalam file
def save_active_proxies(active_proxies, output_file):
    with open(output_file, "w") as file:
        for proxy_type, proxy_address in active_proxies:
            file.write(f"{proxy_type}://{proxy_address}\n")

# Fungsi utama untuk memeriksa proxy
def check_proxies(proxies_list):
    active_proxies = []

    # Loop melalui daftar proxy dan uji masing-masing
    for proxy in proxies_list:
        if "://" in proxy:
            proxy_type, proxy_address = proxy.split("://")
        else:
            proxy_type = "http"
            proxy_address = proxy

        # Status Proxy Jika aktif dan tidak aktif
        if test_proxy(proxy_address, proxy_type):
            print(Fore.GREEN + f"{proxy} IS ACTIVE" + Style.RESET_ALL)
            active_proxies.append((proxy_type, proxy_address))
        else:
            print(Fore.RED + f"{proxy} !!" + Style.RESET_ALL)

    # Simpan proxy yang aktif ke dalam file
    save_active_proxies(active_proxies, output_file)

    # Output hasil (opsional)
    print("\nActive Proxies (saved to file):")
    for proxy_type, proxy_address in active_proxies:
        print(f"{proxy_type}://{proxy_address}")

# Menu utama
def main():
    clear_terminal()
    print(banner)
    time.sleep(2)
    print("Select mode:")
    print("1. Scan from API")
    print("2. Manual from active_proxies.txt")
    print("3. Manual from custom file")
    print("4. Check single proxy manually")
    mode = input("Enter mode (1/2/3/4): ")

    proxies_list = []
    if mode == "1":
        print("Fetching proxies from API...")
        proxies_list = fetch_proxies_from_api(proxy_api_url)
    elif mode == "2":
        print("Reading proxies from proxies.txt...")
        proxies_list = read_proxies(proxy_file)
    elif mode == "3":
        filename = input("Enter filename: ").strip()
        try:
            proxies_list = read_proxies(filename)
        except FileNotFoundError:
            print(Fore.RED + f"File {filename} not found!" + Style.RESET_ALL)
            return
    elif mode == "4":
        proxy_input = input("Enter proxy (e.g. 1.1.1.1:80 or socks5://1.1.1.1:80): ").strip()
        
        # Parsing input
        if "://" in proxy_input:
            proxy_type, proxy_address = proxy_input.split("://")
        else:
            parts = proxy_input.split(":", 1)
            if len(parts) > 1 and parts[0] in ["http", "socks4", "socks5"]:
                proxy_type = parts[0]
                proxy_address = parts[1]
            else:
                proxy_type = "http"
                proxy_address = proxy_input
                
        proxies_list = [f"{proxy_type}://{proxy_address}"]
    else:
        print(Fore.RED + "Invalid mode selected" + Style.RESET_ALL)
        return

    if proxies_list:
        check_proxies(proxies_list)
    else:
        print(Fore.RED + "No proxies to check" + Style.RESET_ALL)

if __name__ == "__main__":
    main()

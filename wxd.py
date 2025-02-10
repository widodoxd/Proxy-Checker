import requests
import requests[socks]
from colorama import Fore, Style, init

# Inisialisasi colorama
init()

# File yang berisi daftar proxy
proxy_file = "proxies.txt"

# File untuk menyimpan proxy yang aktif
output_file = "active_proxies.txt"

# URL yang akan diakses untuk menguji proxy
test_url = "http://google.com"  # Ganti dengan URL yang lebih ringan jika perlu

# Fungsi untuk membaca daftar proxy dari file
def read_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.read().splitlines()
    return proxies

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

        response = requests.get(test_url, proxies=proxies, timeout=2)  # Timeout lebih pendek
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException as e: # Tangani exception request
        #print(f"Error testing {proxy}: {e}") #Print error untuk debugging
        pass
    return False

# List untuk menyimpan proxy yang aktif beserta jenisnya
active_proxies = []

# Baca daftar proxy dari file
proxies_list = read_proxies(proxy_file)

# Loop melalui daftar proxy dan uji masing-masing
for proxy in proxies_list:
    if "://" in proxy:
        proxy_type, proxy_address = proxy.split("://")
    else:
        proxy_type = "http"
        proxy_address = proxy

    # Status Proxy  Jika  aktif dan tidal aktif
    if test_proxy(proxy_address, proxy_type):
        print(Fore.GREEN + f"{proxy} IS ACTIVE" + Style.RESET_ALL) # Output langsung
        active_proxies.append((proxy_type, proxy_address))
    else:
        print(Fore.RED + f"{proxy} !!" + Style.RESET_ALL) # Output langsung

# Simpan proxy yang aktif ke dalam file
with open(output_file, "w") as file:
    for proxy_type, proxy_address in active_proxies:
        file.write(f"{proxy_type}://{proxy_address}\n")

# Output hasil (opsional, bisa dihilangkan jika tidak perlu)
print("\nActive Proxies (saved to file):")
for proxy_type, proxy_address in active_proxies:
    print(f"{proxy_type}://{proxy_address}")



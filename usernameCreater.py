import requests, os, platform
from termcolor import colored

system = platform.system()
clear = "clear" if system == "Linux" else "cls"

def Lower(text):
    text = text.lower()
    text = text.replace("ö", "o")
    text = text.replace("ü", "u")
    text = text.replace("ç", "c")
    text = text.replace("ğ", "g")
    text = text.replace("ş", "s")
    text = text.replace("ı", "i")
    validChars = "abcdefghijklmnopqrstuvwxyz"
    new = ""
    for t in text:
        if t in validChars: new+=t
    return new

def Check(uname, csrf):
    payload = {
        "email": "",
        "first_name":"",
        "username": uname,
        "opt_into_one_tap": False
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    response = requests.post("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", data=payload, headers=login_header)

    if "username_is_taken" in response.text: 
        print(colored(f"{uname} -> Unavailable", "light_red"))
        return False
    else: 
        print(colored(f"{uname} -> Available", "light_green"))
        return True

def Shorter(surname):
    if "aydin" in surname:
        x = surname.replace("aydin", "aydn")
        return x
    elif "ozcan" in surname:
        x = surname.replace("ozcan", "ozcn")
        return x
    elif "erdem" in surname:
        x = surname.replace("erdem", "erdm")
        return x
    elif len(surname) == 5:
        s = surname[0::2]
        for i in s:
            if i in "aeiou": return ""
        return s
    elif "yilmaz" in surname:
        x = surname.replace("yilmaz", "ylmaz")
        return x
    elif "yildiz" in surname:
        x = surname.replace("yildiz", "yldz")
        return x
    elif "yildirim" in surname:
        x = surname.replace("yildirim", "yildrm")
        return x
    else: return ""

print(colored('İsminizi Giriniz: ', 'light_yellow'), end="")
name = Lower(input())
print(colored('Soyadınızı Giriniz: ', 'light_yellow'), end="")
surname = Lower(input(""))

link = "https://www.instagram.com/accounts/emailsignup/"
response = requests.get(link)
csrf = response.cookies["csrftoken"]

uNames = []
sNames = [surname]
surname2 = Shorter(surname)
if surname2 != "":
    print(colored(f"{surname2.upper()} kısaltmasının kullanılmasını istiyor musunuz? (Y/n): ", 'light_yellow'), end="")
    sname = input().lower().replace(" ", "")
    if sname == "y" or sname == "": sNames.append(surname2)

for surname in sNames:
    if Check(name+surname, csrf):
        uNames.append(name+surname)
    else:
        check_ = name+surname+"_"
        if Check(check_, csrf): uNames.append(check_)
        else:
            check_ += check_[-1]
            if Check(check_, csrf): uNames.append(check_)
        
        check_ = name+surname+surname[-1]
        if Check(check_, csrf): uNames.append(check_)
        else:
            check_ += "_"
            if Check(check_, csrf): uNames.append(check_)
        
        check_ = name+name[-1] + surname
        if Check(check_, csrf): uNames.append(check_)
        else:
            check_ += "_"
            if Check(check_, csrf): uNames.append(check_)

    if name.count("e") != 0:
        currentName = name.replace("e", "3", 1)
        check_ = currentName+surname
        if Check(check_, csrf): uNames.append(check_)

    ogeler = [".", "-", "_"]
    for oge in ogeler:
        check_ = name+oge+surname
        if Check(check_, csrf): uNames.append(check_)

    if name.count("e") != 0:
        for oge in ogeler:
            check_ = currentName+oge+surname
            if Check(check_, csrf): uNames.append(check_)

os.system(clear)
print(colored(f"Kullanılabilir Kullanıcı Adları;", 'white'))
count = 0
for uname in uNames:
    color = "light_green" if count %2 == 0 else "light_cyan"
    print(colored("     " + uname, color))
    count+=1
print(colored(f"Eleme yapmak ister misiniz? (Y/n): ", 'light_yellow'), end="")
yardim = input().replace(" ", "").lower()
if yardim == "y" or yardim == "":
    os.system(clear)
    count = 1
    for uname in uNames:
        color = "light_green" if count %2 == 0 else "light_cyan"
        print(colored(f"    {count}) {uname}", color))
        count+=1
    print(colored("* Elemek istediğiniz kullanıcı adlarını virgül kullanarak girin:", 'white'))
    print(colored("örnek: 1,4,7,9", "cyan"))
    print(colored("Elemek istedikleriniz: ", 'light_yellow'), end="")
    elek = input().replace(" ", "")
    elek = elek.split(",")
    count = 0
    for i in elek:
        uNames.remove(uNames[int(i)-1-count])
        count+=1

    count = 0
    for uname in uNames:
        color = "light_green" if count %2 == 0 else "light_cyan"
        print(colored("     " + uname, color))
        count+=1
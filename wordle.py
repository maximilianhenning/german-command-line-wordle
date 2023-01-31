import requests
import string
import random
from bs4 import BeautifulSoup

leipzig = requests.get("https://pcai056.informatik.uni-leipzig.de/downloads/etc/legacy/Papers/top10000de.txt")
words_all = leipzig.text.splitlines()
hermit = requests.get("https://github.com/hermitdave/FrequencyWords/raw/master/content/2016/de/de_50k.txt")
hermit = hermit.text.splitlines()
hermit = [line.split()[0] for line in hermit]
words_all += hermit

name_list = []
def name_scraper(link):
    names_page = requests.get(link)
    names_html = names_page.text
    soup = BeautifulSoup(names_html, "html.parser")
    name_items = soup.find_all("li")
    for item in name_items:
        name_link = item.find("a")
        if name_link:
            name = name_link.get("title")
        if name:
            name_list.append(name.lower())
    return name_list
names_male = name_scraper("https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_h%C3%A4ufigsten_m%C3%A4nnlichen_Vornamen_Deutschlands")
names_female = name_scraper("https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_h%C3%A4ufigsten_weiblichen_Vornamen_Deutschlands")
name_list += names_male, names_female
for name in name_list:
    if name in words_all:
        words_all.remove(name)

def acceptable(word):
    for char in word:
        if char in string.punctuation:
            return False
    if not len(word) == 5:
        return False
    return True
words = [word.lower() for word in words_all if acceptable(word)]
word = words[random.randrange(1, len(words))]

def checker(input):
    char = 0
    line_check = ""
    char_list = []
    while char < 5:
        if user_input[char] == word[char]:
            line_check += "X"
        elif user_input[char] in word:
            line_check += "x"
        else:
            line_check += "-"
        if user_input[char] not in char_list:
            char_list.append(user_input[char])
        char += 1
    return line_check, char_list

gameover = False
while gameover == False:
    tries = 1
    won = False
    output = ""
    used_chars = []
    while tries < 6:
        while True:
            user_input = input(str(tries) + ". Versuch: ")
            user_input = user_input.lower()
            if len(user_input) == 5:
                if user_input in words:
                    break
                else:
                    print("Kein gültiges Wort.")
                    continue
            else:
                print("Dein Versuch muss fünf Zeichen lang sein.")
                continue
        line_check, char_list = checker(user_input)
        used_chars += char_list
        used_chars = list(set(used_chars))
        used_chars.sort()
        output += str("\n            " + line_check)
        if tries > 1:
            print("Benutzte Zeichen: " + str(used_chars))
        print(output)
        if line_check == "XXXXX":
            tries += 10
            won = True
            gameover = True
            break
        else:
            tries += 1
    if won == True:
        print("Herzlichen Glückwunsch!")
        input()
    else:
        print("Leider kein Erfolg! Das Wort war " + word)
        input()
    gameover = True
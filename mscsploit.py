#!python

# TODOs:
# make args in mscsploit

from bs4 import BeautifulSoup
from art import tprint

import html
import os
import re
import requests

FOLDER = '\\Documents\\Human Systems\\CVS\\' #Beggining with ~
# FOLDER = '/Documents/' # For linux

HEADERS = headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

def choose_batch():
    batches = [
	    [1, '2022', 'https://msc-mu.com/level/17'],
        [2, 'Rou7', 'https://msc-mu.com/level/16'],
        [3, 'Wateen', 'https://msc-mu.com/level/15'],
        [4, 'Nabed', 'https://msc-mu.com/level/14'],
        [5, 'Wareed', 'https://msc-mu.com/level/13']
    ]
    print('\n')
    for batch in batches:
        print(str(batch[0]) + ') ' + batch[1] )
    ui_batch = input('\n[*] Which batch are you?\n\n>> ')
    try:
        ui_batch = int(ui_batch)
        for batch in batches:
            if ui_batch == batch[0]:
                print('\n[*] Searching', batch[1] + '\'s batch...\n')
        batch_url = batches[ui_batch - 1][2]
        return batch_url
    except:
        print('\n[*]Invalid Input\n')
        return choose_batch()

def find_courses(url):
    page = requests.get(url, headers=HEADERS)
    doc = BeautifulSoup(page.text, 'html.parser')
    subject = doc.find_all('h6')
    courses = []
    x = 0
    for i in subject:
        x += 1
        parent = i.parent.parent.parent
        course_number = re.findall('href="https://msc-mu.com/courses/(.*)">', parent.decode())[0]
        course_name = i.string.strip()
        courses.append([x, course_name, course_number])
    return courses

def find_subject_folder(name, doc):
    if '&amp;' in name:
        name = html.unescape(name)
    folder_source = doc.find_all("a", string=name)[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent
    folder = re.findall('''</i>
                    (.*)

                </h6>''', folder_source.decode())
    return folder[0]

def choose_course(url):
    global courses
    courses = find_courses(url)
    for course in courses:
        print(str(course[0]) + ') ' + course[1])
    ui_course = input('\n[*] Which course would you like to download?\n\n>> ')
    try:
        ui_course = int(ui_course)
        for course in courses:
            if ui_course == course[0]:
                list_index = ui_course - 1
                print('\n[*] Downloading', course[1])
        course_number = str(courses[list_index][2])
        return course_number
    except:
        print('\n[*]Invalid Input\n')
        return choose_course(url)

def download_lectures(url, folder, folder_url):
    course_page = requests.get(url, headers=HEADERS)
    links = re.findall('<a href="(.*)">.*.pdf</a>', course_page.content.decode())
    names = re.findall('<a href=".*">(.*).pdf</a>', course_page.content.decode())
    page = requests.get(folder_url, headers=HEADERS)
    doc = BeautifulSoup(page.text, 'html.parser')
    x=0
    y=0
    prev_sub_folder = None
    for link in links:
        link = link.strip() + '.pdf'
        subject_folder = find_subject_folder(names[x] + '.pdf', doc)
        if subject_folder == prev_sub_folder:
            pass
        else:
            y = 0 
        new_name = str(y+1) + '. ' + names[x] + '.pdf'
        x += 1
        y += 1
        prev_sub_folder = subject_folder
        if os.path.isfile(folder + subject_folder + '/' + new_name):
            if new_name[0] == '1' and new_name[1] == '.':
                print('\n################ ' + subject_folder + ' ################\n')
            print(' ' + new_name + ' <is already downloaded there XD>')
            continue
        ## FOR LINUX USERS
        # os.system('wget ' + link + ' -O \'' + folder  +'/'+ new_name + '\'')
        os.system('curl ' + link + ' --create-dirs -o \'' + folder + subject_folder +'/'+ new_name + '\'')
        # if os.path.isdir(folder+subject_folder) == False:
        #     os.system('powershell -c "mkdir \'' + folder + subject_folder + '\'"')
        # os.system('powershell -c "Invoke-Webrequest -Uri ' + link + ' -OutFile \'' + folder + subject_folder + '\\' + new_name + '\'"') 
        print('[*] Downloaded ' + new_name)
         
def choose_folder():
    # folder = os.path.expanduser("~") + FOLDER
    ## FOR LINUX USERS
    folder = os.path.expanduser("~") + FOLDER
    answer = input('[*] Your default destination is ' + folder +  "\n[*] Do you want to change that (N/y): ")

    if answer == 'y' or answer == 'yes':
        valid_folder = False
        while valid_folder == False:
            ui_folder = input('\n[*] Enter the Folder you want to save material in.\n\n>> ')
            if os.path.isdir(ui_folder):
                folder = ui_folder
                valid_folder = True
            else:
                print('\n[*] Folder Not found! ', end='')
    return folder

def main():
    folder = choose_folder()
    batch_url = choose_batch()
    course_number = choose_course(batch_url)

    global download_url 
    download_url = 'https://msc-mu.com/courses/' + course_number
    download_lectures(download_url, folder, download_url)

if __name__ == '__main__':
    print('#'*54)
    tprint('M5C5PL017')
    print('#'*54, end='\n\n')
    
    try:
        main()
    except KeyboardInterrupt:
        print('\n[*] Good bye!')
        quit()

    print('\n\n[*] Done...')
    print('[*] Goodbye!')
    input('[*] Press anything to exit')
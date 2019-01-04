from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
from datetime import datetime


'''
use timestring
https://stackoverflow.com/questions/466345/converting-string-into-datetime
'''



def regexcleaner(rawstring) :
    return str((re.sub("\'|\]|\\[", "", rawstring)))

def regexcleaner1(rawstring) :
    return str((re.sub("\'|\]|\\[|\\,", "", rawstring)))

# here's where I found information on exception handling:
# https://stackoverflow.com/questions/8293086/python-continue-iteration-of-for-loop-on-exception
# https://stackoverflow.com/questions/18982610/difference-between-except-and-except-exception-as-e-in-python


url = 'https://web.archive.org/web/20170904175537/http://ldzl.people.com.cn/dfzlk/front/personPage16164.htm'
# functional: https://web.archive.org/web/20170904175537/http://ldzl.people.com.cn/dfzlk/front/personPage16164.htm
# broken: https://web.archive.org/web/20150413115724/http://ldzl.people.com.cn/dfzlk/front/personPage8491.htm

#get the web page
page = requests.get(url)

#creates a new BS holder based on the URL
soup = BeautifulSoup(page.text, 'lxml')

# this is the name section
try:
    name_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
    name_cut = name_unparsed.split('，')
    name_unsliced = name_cut[0]
    #this next thing is to remove the <p> tag from the front of the dude's name. it just slices off the first three characters in the string
    name = name_unsliced [3:]
    print(name)
except Exception as e:
    print ('Error:', e)
    pass

# this gets the person's job title(s) and rank_indiv (which is the relative ranking of each person's titles, based on the order in which they appear)
# it just finds the first instance of this thing because it appears twice on the page
try:
    for entry in soup.find("span", {"class": "red2"}):
        #breaks up the titles if there are multiple titles for the one peson
        if '，' in entry:
            title_split_temp = entry.split('，')
            if '、' in title_split_temp:
                title_split= title_split_temp.split('、').split('、')
        elif '、' in entry:
            title_split = entry.split('、')
        else:
            title_split = [entry]
        #adds the titles to a list of dictionaries for writing later
        #this list of dics will have title:rank_indiv
        title_list = {}
        for item in title_split:
            title_list[(title_split.index(item)+1)] = item
        print(title_list)
except Exception as e:
    print ('Error:', e)
    pass

# this is the gender section
try:
    gender = soup.find('p').contents[1]
    print(gender)
except Exception as e:
    print ('Error:', e)
    pass

# this is the ethnicity section
try:
    ethnicity_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
    eth_cut = ethnicity_unparsed.split('，')
    ethnicity = eth_cut[2]
    print(ethnicity)
except Exception as e:
    print ('Error:', e)
    pass

#this is the dob section
try:
    dob_unparsed = soup.find('p').contents[5]
    dob_year = dob_unparsed[0:4]
    print(dob_year)
    dob_month = dob_unparsed[5:7]
    print(dob_month)
except Exception as e:
    print ('Error:', e)
    pass

# this is the birth_province and birth_place section
try:
    birth_location_unparsed = soup.find('p').contents[9]
    birth_province = birth_location_unparsed[0:2]
    print(birth_province)
    birth_place = birth_location_unparsed[2:4]
    print(birth_place)
except Exception as e:
    print ('Error:', e)
    pass

# this is the education section
try:
    education = soup.find('p').contents[13]
    print(education)
except Exception as e:
    print ('Error:', e)
    pass

# this is to catalogue the date the information was archived by IA
try:
    date_archived_raw = str(re.findall(r"(?<=FILE ARCHIVED ON ).*?(?= AND RETRIEVED)", str(soup)))
    date_archived_processed = regexcleaner1(date_archived_raw)
    date_archived_split = (date_archived_processed[9:])
    date_archived = datetime.strptime(date_archived_split, '%b %d %Y')
    print(date_archived)
except Exception as e:
    print ('Error:', e)
    pass

# this is to catalogue the date we scraped the information
try:
    date_scraped_raw = str(re.findall(r"(?<=INTERNET ARCHIVE ON ).*?(?=\.)", str(soup)))
    date_scraped_processed = regexcleaner1(date_scraped_raw)
    date_scraped_split = (date_scraped_processed[9:])
    date_scraped = datetime.strptime(date_scraped_split, '%b %d %Y')
    print(date_scraped)
except Exception as e:
    print ('Error:', e)
    pass



## TODO WHEN THIS IS IMPORTED TO THE FULL SCRAPER, A UID COUNTER WILL NEED TO BE ADDED ABOVE AND BELOW, AND THE UID WILL NEED TO BE ADDED TO THE IMAGE NAME



# this is the picture section
try:
    img_url_unparsed = str(soup.find('img', {'id': 'userimg'}))
    img_url_end = img_url_unparsed.split('"')[7]
    img_url = 'https://web.archive.org' + img_url_end
    print(img_url)
except Exception as e:
    print ('Error:', e)
    pass

try:
    #I assume this will be a dynamically created variable
    url_save_file_name = name + '_' + dob_unparsed + '.jpg'
    #uses requests to download the picture
    image_r = requests.get(img_url, allow_redirects=True)
    #writes the downloaded picture to the file
    open(url_save_file_name, 'wb').write(image_r.content)
    print(url_save_file_name + " saved")
except Exception as e:
    print ('Error:', e)
    pass

#this is the person's CV as listed at the bottom of the page, pulled in full then cleaned up to strip out unnecessary characters/tags
try:
    data_dump = str(soup.find('div', {'class', 'p2j_text'}))
    full_person_resume = str((re.sub("<p>|</p>|<div class=\"p2j_text\">|</div>", "", data_dump)))
    print(full_person_resume)
except Exception as e:
    print ('Error:', e)
    pass

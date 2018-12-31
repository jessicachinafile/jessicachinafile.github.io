from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re


# TODO ASSIGN UIDS
# TODO what about error handling when a page is missing?
# TODO convert date_archived and date_scraped to date format
# TODO make sure image gets named by UID


# TODO: pull date last updated from url once the page loads


def regexcleaner(rawstring) :
    return str((re.sub("\'|\]|\\[", "", rawstring)))

url = 'https://web.archive.org/web/20171212033200/http://ldzl.people.com.cn:80/dfzlk/front/personPage6129.htm'

#get the web page
page = requests.get(url)

#creates a new BS holder based on the URL
soup = BeautifulSoup(page.text, 'lxml')

# this gets the title and rank_indiv
# it just finds the first instance of this thing because it appears twice on the page
for entry in soup.find("span", {"class": "red2"}):

    #breaks up the titles if there are multiple titles for the one peson
    title = entry
    if '、' in title:
        title_split = title.split('、')
    elif '，' in title:
        title_split = title.split('、')
    else:
        title_split = title

    #adds the titles to a list of dictionaries for writing later
    #this may be something that can be done  more effidiently at the db writing stage
    #I just broke it out  here to make sure I could identify the position properly

    #this list of dics will  have title:rank_indiv
    title_list = {}

    for item in title_split:
        title_list[(title_split.index(item)+1)] = item
    print(title_list)


# this is the name section
name_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
name_cut = name_unparsed.split('，')
name_unsliced = name_cut[0]
#this next thing is to remove the <p> tag from the front of the dude's name. it just slices off the first three characters in the string
name = name_unsliced [3:]
print(name)


# this is the gender section
gender = soup.find('p').contents[1]
print(gender)

#this is the dob section
dob_unparsed = soup.find('p').contents[5]
#print(dob_unparsed)
dob_year = dob_unparsed[0:4]
print(dob_year)
dob_month = dob_unparsed[5:7]
print(dob_month)

# this is the birth_province and birth_place section
birth_location_unparsed = soup.find('p').contents[9]
#print(birth_location_unparsed)
birth_province = birth_location_unparsed[0:2]
print(birth_province)
birth_place = birth_location_unparsed[2:4]
print(birth_place)

# this is the education section
education = soup.find('p').contents[13]
print(education)

# this is the ethnicity section
ethnicity_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
eth_cut = ethnicity_unparsed.split('，')
ethnicity = eth_cut[2]
print(ethnicity)


# this is to catalogue the date the information was archive and the date we scraped it
date_archived_raw = str(re.findall(r"(?<=FILE ARCHIVED ON ).*?(?= AND RETRIEVED)", str(soup)))
date_archived_processed = regexcleaner(date_archived_raw)
date_archived_split = (date_archived_processed[9:])
print(date_archived_split)
date_scraped_raw = str(re.findall(r"(?<=INTERNET ARCHIVE ON ).*?(?=\.)", str(soup)))
date_scraped_processed = regexcleaner(date_scraped_raw)
date_scraped_split = (date_scraped_processed[9:])
print(date_scraped_split)

# this is the picture section
img_url_unparsed = str(soup.find('img', {'id': 'userimg'}))
img_url_end = img_url_unparsed.split('"')[7]
img_url = 'https://web.archive.org' + img_url_end
print(img_url)


#I assume this will be a dynamically created variable
url_save_file_name = name + '_' + dob_unparsed + '.jpg'
#uses requests to download the picture
image_r = requests.get(img_url, allow_redirects=True)
#writes the downloaded picture to the file
open(url_save_file_name, 'wb').write(image_r.content)

#this is the person's CV as listed at the bottom of the page, pulled in full then cleaned up to strip out unnecessary characters/tags
data_dump = str(soup.find('div', {'class', 'p2j_text'}))
data_cleaned = str((re.sub("<p>|</p>|<div class=\"p2j_text\">|</div>", "", data_dump)))
print(data_cleaned)

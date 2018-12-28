from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re

##############################################################
#############THIS GETS LINKS TO EACH PROVINCE PAGE####################
##############################################################

url = 'https://web.archive.org/web/20171224064640/http://ldzl.people.com.cn:80/dfzlk/front/personProvince1028.htm'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# a function to remove all the extra crap regex adds to lines -- here's where I found how to do that: https://www.tutorialspoint.com/How-to-remove-specific-characters-from-a-string-in-Python
def regexcleaner(rawstring) :
    return str((re.sub("\'|\]|\\[", "", rawstring)))



#initializes the dictionary
province_dict = {}

# extracts the list of provinces from the block on the left side of the page
for entry in soup.find_all("div", {"class": "fl nav_left_2j"}):
    #breaks out each province list item
    for item in entry.find_all("li"):
        link = item.find('a').get('href')
        #there is no link for the Taiwan entry so this pulls it out to avoid an error
        if link == None:
            full_link = 'Taiwan.tw'
        #for the rest of the links, makes them a full URL
        else:
            full_link = 'https://web.archive.org' + link
        #extracts the name of the province
        province = item.get_text()
        #adds entry to the dictionary
        province_dict[province] = full_link

#cleans up the dictionary by removing renegade provinces
del province_dict['台湾省']
del province_dict['澳门特别行政区']
del province_dict['香港特别行政区']


pprint(province_dict)


#######################################################################
###### THIS PULLS THE PERSON INFO WE WANT ON EACH PROVINCE PAGE #######
#######################################################################

#this will be the loop structure once you get it right
'''for province in province_dict:
    province_url = province_dict[province]
    province_page = requests.get(province_url)
    province_soup = BeautifulSoup(province_page.txt)'''


'''
url = province_dict['安徽省']
province_page = requests.get(url)
province_soup = BeautifulSoup(province_page.text, 'lxml')
'''


province_url = 'https://web.archive.org/web/20171224064640/http://ldzl.people.com.cn:80/dfzlk/front/personProvince1028.htm'

province_page = requests.get(province_url)
province_soup = BeautifulSoup(province_page.text, 'lxml')


# grabs name of province of the page we're working on
province_name_raw = str(province_soup.findAll('h1'))
province_name = str(re.findall(r">(.*?)<", province_name_raw))


# pulls the names and urls for the guys listed near the top of the page (the ones that have the pictures)
province_picguys_raw = str([dd.find('a') for dd in province_soup.findAll('dd')])
# because of messed up formatting below for the nopicguys, we need to make sure the formatting of the picguys output is the same as the formatting of the nopicguys output so we can de-dupe later.
province_picguys = re.findall(r"(?<==\").*?(?=</a>)", province_picguys_raw)

# pulls the names and urls for the guys listed below the picguys, who don't have pictures and are in the section that breaks them out by party/govt. unfortunately because of annoying quotation marks and other bad html, BeautifulSoup doesn't see the <a> tags, which means we're going to first use BS to pull all the <p> tags and then use regex to get us the <a> tag stuff.
province_nopicguys_raw = str(province_soup.findAll('p'))
province_nopicguys = re.findall(r"(?<==\").*?(?=</a>)", province_nopicguys_raw)
# combines picguys and nopicguys into one ordered list
province_official_name_url_raw = province_picguys + province_nopicguys


#creates an empty dictionary for us to fill at bottom of loop
province_officials_dict = {}

# creates an empty list we can fill in a sec
province_offical_name_url_deduped  = []

# The base rank number -- it will iterate through for each entry in the list and add one, thereby ranking everyone in order
provincepage_rankpeer = 1

# goes through the combined list in order and checks to see if each entry is already in the empty list we just created. if not, it adds it. if so, then it skips it.
for item in province_official_name_url_raw :
    if item not in province_offical_name_url_deduped:
        province_offical_name_url_deduped.append(item)
    else :
        pass

# Generates the pool by getting the number of entries in the list created by province_offical_name_url_deduped
provincepage_poolpeer = len(province_offical_name_url_deduped)

for item in province_offical_name_url_deduped :
    item_string = str(item)

    #pulls url for each person and then cleans it up using function we defined up top
    province_official_url_raw = str(re.findall(r"^(.*?)\"", item_string))
    province_official_url_cleaned = regexcleaner(province_official_url_raw)
    #makes url complete by adding prefix (internet archive will change date in url to load to last time page was scraped, so we chose a date at end of 2018 to ensure it was post-scraping)
    province_official_url = 'https://web.archive.org/web/20181226105432/http://ldzl.people.com.cn:80/dfzlk/front/' + province_official_url_cleaned

    #pulls out each person's name and then cleans up the regex result
    province_official_name_raw = str(re.findall(r"\>(.*?)$", item_string))
    province_official_name = regexcleaner(province_official_name_raw)

    # since we'll have to nest dictionaries, this creates a temporary (nested) dictionary for each iteration of the loop
    holder_dict = {}
    holder_dict["url"] = province_official_url
    holder_dict["pool"] = provincepage_poolpeer
    holder_dict["rank"] = provincepage_rankpeer

    # this creates the big dictionary, that matches each person's name with their temporary dictionary information
    province_officials_dict[province_official_name] = holder_dict

    # this adds 1 to the rank for the next iteration of the loop
    provincepage_rankpeer +=1

pprint(province_officials_dict)




##############################################################
###### THIS PULLS CITY NAME AND URL FOR NEXT LOOP/STEP #######
##############################################################


city_dict = {}

# pulls the names and urls for each city under this particular province
for entry in province_soup.find_all("ol", {"class": "fl"}):
    for item in entry.find_all("span"):
        if "href" in str(item) :
            item_string = str(item)

            #pulls city url and then cleans regex result
            city_url_raw = str(re.findall(r"(?<=href=\").*?(?=\")", item_string))
            city_url_cleaned = regexcleaner(city_url_raw)
            # makes it a full url
            city_url = 'https://web.archive.org' + city_url_cleaned

            #pulls city name and then cleans the regex result
            city_name_raw = str(re.findall(r"(?<=信息\">).*?(?=<)", item_string))
            city_name = regexcleaner(city_name_raw)

            # writes city names and urls to dictionary
            city_dict[city_name] = city_url

        else :
            pass

pprint(city_dict)

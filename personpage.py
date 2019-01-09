from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
from datetime import datetime
import pandas as pd

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


url = 'https://web.archive.org/web/20150329235635/http://ldzl.people.com.cn/dfzlk/front/personPage4097.htm'
# functional: https://web.archive.org/web/20170904175537/http://ldzl.people.com.cn/dfzlk/front/personPage16164.htm
# broken: https://web.archive.org/web/20150413115724/http://ldzl.people.com.cn/dfzlk/front/personPage8491.htm
# shanxi super broken: https://web.archive.org/web/20150413123909/http://ldzl.people.com.cn/dfzlk/front/personPage5855.htm
# hebei broken: https://web.archive.org/web/20150329235635/http://ldzl.people.com.cn/dfzlk/front/personPage4097.htm

#get the web page
page = requests.get(url)

#creates a new BS holder based on the URL
soup = BeautifulSoup(page.text, 'lxml')

# creates a list where we can add all the information about each official to get converted/printed to a csv
prov_official_csv_holder = []

# this is the name section
try:
    name_raw = str([dd.find('em') for dd in soup.findAll('dd')])
    name_processed = re.findall(r"(?<=<em>).*?(?=</em>)", name_raw)
    name = regexcleaner(str(name_processed))
    # THe NEXT 4 LINES ARE PREVIOUS CODE TO GET THE NAMES, LEFT HERE IN CASE NEEDED
    # name_unparsed = str(soup.find('div', {'class': # 'p2j_text'}).contents[1])
    # name_cut = name_unparsed.split('，')
    # name_unsliced = name_cut[0]
    # name = name_unsliced [3:]
    print(name)
except Exception as e:
    print ('Error:', e)
    name = 'Error:', e
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
    title_list = 'Error:', e
    pass

# this breaks the title_list into discrete titles (still in order) for writing to the csv later
number_of_titles = len(title_list)
if number_of_titles > 1 :
    title_2 = title_list[2]
else :
    title_2 = ("")
if number_of_titles > 2 :
    title_3 = title_list[3]
else :
    title_3 = ("")
if number_of_titles > 3:
    title_4 = title_list[4]
else :
    title_4 = ("")


# this is the gender section
try:
    gender = soup.find('p').contents[1]
    print(gender)
except Exception as e:
    print ('Error:', e)
    gender = 'Error:', e
    pass

# this is the ethnicity section
try:
    ethnicity_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
    eth_cut = ethnicity_unparsed.split('，')
    ethnicity = eth_cut[2]
    print(ethnicity)
except Exception as e:
    print ('Error:', e)
    ethnicity = 'Error:', e
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
    dob_year = 'Error:', e
    dob_month = 'Error:', e
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
    birth_province = 'Error:', e
    birth_place = 'Error:', e
    pass

# this is the education section
try:
    education = soup.find('p').contents[13]
    print(education)
except Exception as e:
    print ('Error:', e)
    education = 'Error:', e
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
    date_archived = 'Error:', e
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
    date_scraped = 'Error:', e
    pass


## TODO WHEN THIS IS IMPORTED TO THE FULL SCRAPER, A UID COUNTER WILL NEED TO BE ADDED ABOVE AND BELOW, AND THE UID WILL NEED TO BE ADDED TO THE IMAGE NAME


# this grabs the url for the person's photo
try:
    img_url_raw = str([dt.find('img') for dt in soup.findAll('dt')])
    img_url_processed = re.findall(r"(?<=src\=\").*?(?=\")", img_url_raw)
    img_url_cleaned = regexcleaner(str(img_url_processed))
    if 'https' not in img_url_cleaned :
        img_url = 'https://web.archive.org' + img_url_cleaned
    else :
        img_url = img_url_cleaned
    # THE NEXT 3 LINES ARE OLD CODE TO GET THE IMAGE URL, LEAVING THEM IN FOR NOW IN CASE NEEDED
    #img_url_unparsed = str(soup.find('img', {'id': 'userimg'}))
    #img_url_end = img_url_unparsed.split('"')[7]
    #img_url = 'https://web.archive.org' + img_url_end
    print(img_url)
except Exception as e:
    print ('Error:', e)
    img_url = 'Error:', e
    pass

# this names and saves the image file
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
    url_save_file_name = 'Error:', e
    pass

#this is the person's CV as listed at the bottom of the page, pulled in full then cleaned up to strip out unnecessary characters/tags
try:
    data_dump = str(soup.find('div', {'class', 'p2j_text'}))
    full_person_resume = str((re.sub("<p>|</p>|<div class=\"p2j_text\">|</div>", "", data_dump)))
    print(full_person_resume)
except Exception as e:
    print ('Error:', e)
    full_person_resume = 'Error:', e
    pass

# DataFrame explanation: https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
# indicates that each row of the pandas DataFrame will consist of these items, as we defined them above
row_holder = [name, title_list[1], title_2, title_3, title_4, gender, ethnicity, dob_year, dob_month, birth_province, birth_place, education, date_archived, date_scraped, img_url, url_save_file_name, full_person_resume]

# adds the row we just created to the holder file we created at top
prov_official_csv_holder.append(row_holder)

# converts the row info into a DataFrame, defines the column and row headings
prov_official_row = pd.DataFrame(prov_official_csv_holder, columns=['Name','Title 1', 'Title 2', 'Title 3', 'Title 4', 'Gender', 'Ethnicity', 'Birth Year', 'Birth Month', "Birth Province", "Birth Place", "Education", "Archived", "Scraped", "Image URL", "Image Filename", "Resume"])

#FOR USE WITH UIDS/INDEXES
#df1 = pd.DataFrame(data, index=['first', 'second'], columns=['a', 'b'])

# writes that DF info to a csv and encodes it so we can read the csv
# TODO HAVE THE CSV INFO APPEND RATHER THAN OVERWRITE
# TODO ONCE THIS IS ON THE BIG PAGE, MAKE SURE THAT THE PROVINCE/COUNTY/ETC GET WRITTEN INTO CSV
prov_official_row.to_csv('new.csv', encoding='utf-8')

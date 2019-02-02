# encoding=utf8

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



# a function to remove all the extra crap regex adds to lines -- here's where I found how to do that: https://www.tutorialspoint.com/How-to-remove-specific-characters-from-a-string-in-Python
def regexcleaner(rawstring) :
    return str((re.sub("\'|\]|\\[", "", rawstring)))

# same function but with a comma added for parsing dates on the personpage
def regexcleaner1(rawstring) :
    return str((re.sub("\'|\]|\\[|\\,", "", rawstring)))

def which_page_function():
    try:
        name_raw = str([dd.find('em') for dd in soup.findAll('dd')])
        name_processed = re.findall(r"(?<=<em>).*?(?=</em>)", name_raw)
        if "input" in str(name_processed):
            return "new"
        else:
            return "old"
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

# these functions are for use on the person page
def name_function():
    try:
        name_raw = str([dd.find('em') for dd in soup.findAll('dd')])
        name_processed = re.findall(r"(?<=<em>).*?(?=</em>)", name_raw)
        return regexcleaner(str(name_processed))
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_name_function():
    try:
        name_raw = str([dd.find('strong') for dd in soup.findAll('dd')])
        name_processed = re.findall(r"(?<=>).*?(?=<)", name_raw)
        return regexcleaner(str(name_processed))
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def gender_function() :
    try:
        return str(soup.find('p').contents[1])
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_gender_function() :
    try:
        return new_page_unparsed[1]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def ethnicity_function() :
    try:
        ethnicity_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
        eth_cut = ethnicity_unparsed.split('，')
        return eth_cut[2]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_ethnicity_function() :
    try:
        return new_page_unparsed[2]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def dob_year_function():
    try:
        dob_unparsed = soup.find('p').contents[5]
        return dob_unparsed[0:4]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_dob_year_function():
    try:
        year_split = new_page_unparsed[3]
        return year_split[0:4]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def dob_month_function():
    try:
        dob_unparsed = soup.find('p').contents[5]
        return dob_unparsed[5:7]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_dob_month_function():
    try:
        month_split = new_page_unparsed[3]
        return month_split[5:7]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def birth_province_function():
    try:
        birth_location_unparsed = soup.find('p').contents[9]
        return birth_location_unparsed[0:2]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_birth_province_function():
    try:
        birth_province_split = new_page_unparsed[4]
        return birth_province_split[0:2]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def birth_place_function():
    try:
        birth_location_unparsed = soup.find('p').contents[9]
        return birth_location_unparsed[2:4]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_birth_place_function():
    try:
        birth_location_split = new_page_unparsed[4]
        return birth_location_split[2:4]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def education_function():
    try:
        return soup.find('p').contents[13]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_education_function():
    try:
        return new_page_unparsed[8]
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def date_archived_function():
    try:
        date_archived_raw = str(re.findall(r"(?<=FILE ARCHIVED ON ).*?(?= AND RETRIEVED)", str(soup)))
        date_archived_processed = regexcleaner1(date_archived_raw)
        date_archived_split = (date_archived_processed[9:])
        return datetime.strptime(date_archived_split, '%b %d %Y')
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def date_scraped_function():
    try:
        date_scraped_raw = str(re.findall(r"(?<=INTERNET ARCHIVE ON ).*?(?=\.)", str(soup)))
        date_scraped_processed = regexcleaner1(date_scraped_raw)
        date_scraped_split = (date_scraped_processed[9:])
        return datetime.strptime(date_scraped_split, '%b %d %Y')
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def personID_function():
    if len(str(PersonID_counter)) == 1 :
        return '0000000' + str(PersonID_counter)
    elif len(str(PersonID_counter)) == 2 :
        return '000000' + str(PersonID_counter)
    elif len(str(PersonID_counter)) == 3 :
        return '00000' + str(PersonID_counter)
    elif len(str(PersonID_counter)) == 4 :
        return '0000' + str(PersonID_counter)
    elif len(str(PersonID_counter)) == 5 :
        return '000' + str(PersonID_counter)
    elif len(str(PersonID_counter)) == 6 :
        return '00' + str(PersonID_counter)
    elif len(str(PersonID_counter)) == 7 :
        return '0' + str(PersonID_counter)
    else :
        return PersonID_counter

def img_url_function():
    try:
        img_url_raw = str([dt.find('img') for dt in soup.findAll('dt')])
        img_url_processed = re.findall(r"(?<=src\=\").*?(?=\")", img_url_raw)
        img_url_cleaned = regexcleaner(str(img_url_processed))
        if 'https' not in img_url_cleaned :
            return 'https://web.archive.org' + img_url_cleaned
        else :
            return img_url_cleaned
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def url_save_file_name_function():
    try:
        url_save_file_name = 'photo_' + str(PersonID) + '.jpg'
        url_save_file_path = 'images/' + url_save_file_name
        #uses requests to download the picture
        image_r = requests.get(img_url, allow_redirects=True)
        #writes the downloaded picture to the file
        open(url_save_file_path, 'wb').write(image_r.content)
        return url_save_file_name
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def resume_function():
    try:
        data_dump = str(soup.find('div', {'class', 'p2j_text'}))
        return str((re.sub("<p>|</p>|<div class=\"p2j_text\">|</div>", "", data_dump)))
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def new_resume_function():
    try:
        data_dump = str(soup.find('div', {'class', 'box01'}))
        return str((re.sub("<br/>|<div class=\"box01\">|</div>", "", data_dump)))
    except Exception as e:
        print ('Error:', e)
        return 'Error:', e
        pass

def title_list_function():
    # this gets the person's job title(s) and rank_indiv (which is the relative ranking of each person's titles, based on the order in which they appear)
    # it just finds the first instance of this thing because it appears twice on the page
    try:
        for entry in soup.find("span", {"class": "red2"}):
            #breaks up the titles if there are multiple titles for the one peson
            title_replace = entry.replace('，', '、')
            if '、' in title_replace:
                title_split = title_replace.split('、')
                #print(title_split)
            else:
                title_split = [entry]
            #adds the titles to a list of dictionaries for writing later
            #this list of dics will have title:rank_indiv
            title_list = {}
            for item in title_split:
                title_list[(title_split.index(item))] = item
            return title_list
    except Exception as e:
        return ('Error:', e)
        title_list['Error'] = e
        pass

# here's where I found information on exception handling:
# https://stackoverflow.com/questions/8293086/python-continue-iteration-of-for-loop-on-exception
# https://stackoverflow.com/questions/18982610/difference-between-except-and-except-exception-as-e-in-python


url = 'https://web.archive.org/web/20171004034402/http://ldzl.people.com.cn/dfzlk/front/personPage15042.htm'
# functional: https://web.archive.org/web/20170904175537/http://ldzl.people.com.cn/dfzlk/front/personPage16164.htm
# broken: https://web.archive.org/web/20150413115724/http://ldzl.people.com.cn/dfzlk/front/personPage8491.htm
# shanxi super broken: https://web.archive.org/web/20150413123909/http://ldzl.people.com.cn/dfzlk/front/personPage5855.htm
# hebei broken: https://web.archive.org/web/20150329235635/http://ldzl.people.com.cn/dfzlk/front/personPage4097.htm


PersonID_counter = 1

#get the web page
page = requests.get(url)

#creates a new BS holder based on the URL
soup = BeautifulSoup(page.text, 'lxml')



# creates a list where we can add all the information about each official to get converted/printed to a csv
prov_official_csv_holder = []

# error handling for pages that weren't archived
unarchived_page = soup.find('div', {'id': 'errorBorder'})
if unarchived_page :
    name = "Not archived"
    title_1 = "Not archived"
    title_2 = "Not archived"
    title_3 = "Not archived"
    title_4 = "Not archived"
    gender = "Not archived"
    ethnicity = "Not archived"
    dob_year = "Not archived"
    dob_month = "Not archived"
    birth_province = "Not archived"
    birth_place = "Not archived"
    education = "Not archived"
    date_archived = "Not archived"
    date_scraped = "Not archived"
    img_url = "Not archived"
    url_save_file_name = "Not archived"
    full_person_resume = "Not archived"

    print(name + "" + gender + "" + education )

# for everything that was archived
else :

    page_type = which_page_function()
    print("page type: " + page_type)

    if page_type == "old":

        name = name_function()
        print(name)

        gender = gender_function()

        ethnicity = ethnicity_function()

        dob_year = dob_year_function()

        dob_month = dob_month_function()

        birth_province = birth_province_function()

        birth_place = birth_place_function()

        education = education_function()

        full_person_resume = resume_function()

    else:

        new_page_unparsed = (str(soup.find('div', {'class': 'box01'}).contents[0])).split('，')

        name = new_name_function()
        print(name)

        gender = new_gender_function()

        ethnicity = new_ethnicity_function()

        dob_year = new_dob_year_function()

        dob_month = new_dob_month_function()

        birth_province = new_birth_province_function()

        birth_place = new_birth_place_function()

        education = new_education_function()

        full_person_resume = new_resume_function()


    title_list = title_list_function()
    print(title_list)

    #  HOW TO WRITE THIS AS A FUNCTION?
    # this breaks the title_list into discrete titles (still in order) for writing to the csv later
    if title_list is None:
        title_1 = ("None given")
        title_2 = ("")
        title_3 = ("")
        title_4 = ("")
    else:
        number_of_titles = len(title_list)
        if number_of_titles == 1 :
            title_1 = title_list[0]
            title_2 = ("")
            title_3 = ("")
            title_4 = ("")
        elif number_of_titles == 2 :
            title_1 = title_list[0]
            title_2 = title_list[1]
            title_3 = ("")
            title_4 = ("")
        elif number_of_titles == 3 :
            title_1 = title_list[0]
            title_2 = title_list[1]
            title_3 = title_list[2]
            title_4 = ("")
        elif number_of_titles == 4 :
            title_1 = title_list[0]
            title_2 = title_list[1]
            title_3 = title_list[2]
            title_4 = title_list[3]
        else :
            pass

    date_archived = date_archived_function()

    date_scraped = date_scraped_function()

    PersonID = personID_function()

    img_url = img_url_function()

    url_save_file_name = url_save_file_name_function()

'''
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
'''

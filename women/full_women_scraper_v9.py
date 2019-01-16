from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
from datetime import datetime
import pandas as pd


# TODO PROVS AND CITIES NOW ALL WRITE TO SAME CSV. JUST NEED TO INTEGRATE COUNTY PERSON SCRAPER
# TODO need to write something separate for effed up pages?
# TODO ask M for help with title_list function, and with the city df creation being messed up


# TODO - WRITE IN THE READ-ME THAT IT ASSUMES AN 'IMAGES' FOLDER IN THE SAME DIRECTORY

##############################################################
#############THIS GETS LINKS TO EACH PROVINCE PAGE####################
##############################################################

url = 'https://web.archive.org/web/20171224064640/http://ldzl.people.com.cn:80/dfzlk/front/personProvince1028.htm'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# a function to remove all the extra crap regex adds to lines -- here's where I found how to do that: https://www.tutorialspoint.com/How-to-remove-specific-characters-from-a-string-in-Python
def regexcleaner(rawstring) :
    return str((re.sub("\'|\]|\\[", "", rawstring)))

# same function but with a comma added for parsing dates on the personpage
def regexcleaner1(rawstring) :
    return str((re.sub("\'|\]|\\[|\\,", "", rawstring)))

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

def gender_function() :
    try:
        return str(soup.find('p').contents[1])
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

def dob_year_function():
    try:
        dob_unparsed = soup.find('p').contents[5]
        return dob_unparsed[0:4]
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

def birth_province_function():
    try:
        birth_location_unparsed = soup.find('p').contents[9]
        return birth_location_unparsed[0:2]
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

def education_function():
    try:
        return soup.find('p').contents[13]
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
#pprint(province_dict)

print("A. list of provinces generated")
print("")

##############################################################
# so we can limit loops when testing
counter = 1

#creates a list to append all the iterated dictionaries to (each one containing a provincial-level official and his associated information), so they don't keep overwriting each OTHER
#see 'alist' example at: https://stackoverflow.com/questions/23724136/appending-a-dictionary-to-a-list-in-a-a-loop-python
all_prov_officials_dictlist = []
all_city_officials_dictlist = []
all_county_officials_dictlist = []

# tells the scraper to go to each province page and pull all the text from it
for province_name, province_url in province_dict.items() :

    ##############################################################
    #take out this counter line when running for real
    if counter < 3 :
        province_page = requests.get(province_url)
        province_soup = BeautifulSoup(province_page.text, 'lxml')
        ##############################################################
        #take the line below out when you're running this for real
        counter += 1
        #print(province_soup)

#######################################################################
###### THIS PULLS THE PERSON INFO WE WANT ON EACH PROVINCE PAGE #######
#######################################################################


# test province_url = 'https://web.archive.org/web/20171224064640/http://ldzl.people.com.cn:80/dfzlk/front/personProvince1028.htm'


        # grabs name of province of the page we're working on
        province_name_raw = str(province_soup.findAll('h1'))
        province_name_processed = str(re.findall(r">(.*?)<", province_name_raw))
        province_name = regexcleaner(province_name_processed)


        # pulls the names and urls for the guys listed near the top of the page (the ones that have the pictures)
        province_picguys_raw = str([dd.find('a') for dd in province_soup.findAll('dd')])
        # because of messed up formatting below for the nopicguys, we need to make sure the formatting of the picguys output is the same as the formatting of the nopicguys output so we can de-dupe later.
        province_picguys = re.findall(r"(?<==\").*?(?=</a>)", province_picguys_raw)

        # pulls the names and urls for the guys listed below the picguys, who don't have pictures and are in the section that breaks them out by party/govt. unfortunately because of annoying quotation marks and other bad html, BeautifulSoup doesn't see the <a> tags, which means we're going to first use BS to pull all the <p> tags and then use regex to get us the <a> tag stuff.
        province_nopicguys_raw = str(province_soup.findAll('p'))
        province_nopicguys = re.findall(r"(?<==\").*?(?=</a>)", province_nopicguys_raw)
        # combines picguys and nopicguys into one ordered list
        province_official_name_url_raw = province_picguys + province_nopicguys

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

        #creates an empty dictionary for us to fill at bottom of loop
        province_officials_dict = {}

        for item in province_offical_name_url_deduped :
            item_string = str(item)

            #pulls url for each person and then cleans it up using function we defined up top
            province_official_url_raw = str(re.findall(r"^(.*?)\"", item_string))
            province_official_url_cleaned = regexcleaner(province_official_url_raw)
            #makes url complete by adding prefix (internet archive will change date in url to load to last time page was scraped, so we chose a date at end of 2018 to ensure it was post-scraping)
            province_official_url = 'https://web.archive.org/web/20180526105432/http://ldzl.people.com.cn:80/dfzlk/front/' + province_official_url_cleaned

            #pulls out each person's name and then cleans up the regex result
            province_official_name_raw = str(re.findall(r"\>(.*?)$", item_string))
            province_official_name = regexcleaner(province_official_name_raw)

            # since we'll have to nest dictionaries, this creates a temporary (nested) dictionary for each iteration of the loop
            holder_dict = {}
            holder_dict["url"] = province_official_url
            holder_dict["pool"] = provincepage_poolpeer
            holder_dict["rank"] = provincepage_rankpeer
            holder_dict["province"] = province_name
            holder_dict["city"] = ""
            holder_dict["county"] = ""

            # this creates the dictionary that matches each person's name with their temporary dictionary information
            province_officials_dict[province_official_name] = holder_dict

            # this adds 1 to the rank for the next iteration of the loop
            provincepage_rankpeer +=1

        # then here we append each province's dictionary to the dictionary for all provinces, so that we end up with one big list of provincial-level officials, rather than the last province scraped overwriting everything.
        all_prov_officials_dictlist.append(province_officials_dict)

        #pprint(all_prov_officials_dictlist)
        print("B. " + province_name + " province person list generated")
        print("")

#print(all_prov_officials_dictlist)



#################################################################################
###### THIS PULLS CITY NAME AND URL FROM PROVINCE PAGE FOR NEXT LOOP/STEP #######
################################################################################


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

        #pprint(city_dict)
        print("C. " + province_name + " list of cities generated")
        print("")


        ##############################################################
        # so we can limit loops when testing
        citycounter = 1

        # tells the scraper to go to each city page and pull all the text from it
        for city_name, city_url in city_dict.items() :
            ##############################################################
            #take out this counter line when running for real
            if citycounter < 3 :
                city_page = requests.get(city_url)
                city_soup = BeautifulSoup(city_page.text, 'lxml')


##################################################################################################
#####THIS HARVESTS THE CITY-LEVEL INDIVIDUALS' INFORMATION AT THE TOP OF THE CITY PAGE ###########
###################################################################################################

                # This pulls the person's name and URL. Here's where I found the code to find <a> as nested under specific parent tags: https://stackoverflow.com/questions/1058599/how-to-get-a-nested-element-in-beautiful-soup
                citypage_name_url = [dd.find('a') for dd in city_soup.findAll('dd')]

                # Generates the pool by getting the number of entries in the list created by citypage_name_url
                citypage_poolpeer = len(citypage_name_url)

                # The base rank number -- it will iterate through for each entry in the list and add one, thereby ranking everyone in order
                citypage_rankpeer = 1

                # Creates empty dictionary we can fill later
                citypage_officials_dict = {}

                # parses each item in the list generated by citypage_name_url
                for item in citypage_name_url :

                    # makes each entry in the above list into a string so we can manipulate it
                    item_string = str(item)

                    # uses regex to just pull the information we're looking for -- must also be converted to a string after regex does its thing
                    citypage_urlonly = str(re.findall(r"\"(.*?)\"", item_string))
                    # cleans up the regex result with the function defined at top
                    citypage_urlonly_cleaned = regexcleaner(citypage_urlonly)

                    #makes url complete by adding prefix (internet archive will change date in url to load to last time page was scraped, so we chose a date at end of 2018 to ensure it was post-scraping)
                    city_official_full_url = 'https://web.archive.org/web/20181226105432/http://ldzl.people.com.cn:80/dfzlk/front/' + citypage_urlonly_cleaned

                    citypage_nameonly = str(re.findall(r"\>(.*?)\</", item_string))
                    citypage_nameonly_cleaned = regexcleaner(citypage_nameonly)

                    # since we'll have to nest dictionaries, this creates a temporary (nested) dictionary for each iteration of the loop
                    city_holder_dict = {}
                    city_holder_dict["url"] = city_official_full_url
                    city_holder_dict["pool"] = citypage_poolpeer
                    city_holder_dict["rank"] = citypage_rankpeer
                    city_holder_dict["province"] = province_name
                    city_holder_dict["city"] = city_name
                    city_holder_dict["county"] = ""

                    # this creates the big dictionary, that matches each person's name with their temporary dictionary information
                    citypage_officials_dict[citypage_nameonly_cleaned] = city_holder_dict

                    # this adds 1 to the rank for the next iteration of the loop
                    citypage_rankpeer +=1

                # then here we append each citys dictionary to the dictionary for all cities, so that we end up with one big list of city-level officials, rather than the last city scraped overwriting everything.
                all_city_officials_dictlist.append(citypage_officials_dict)

                print("D. " + province_name + " " + city_name + " city person list generated")
                #pprint(all_city_officials_dictlist)
                print ("")


##################################################################################################
#####THIS HARVESTS THE COUNTY-LEVEL INDIVIDUALS' INFORMATION AT THE BOTTOM OF THE CITY PAGE ######
###################################################################################################


                # Creates empty dictionary we can fill later
                county_dict = {}

                # grabs all the information we're interested in in one big chunk
                citypage_county_listinfo = city_soup.find_all('ol', {'class' : 'fl'})
                #print(str(citypage_county_listinfo) + "\n")

                # unfortunately it has only 2 items in it, the first one of which is useless for us (so we ignore it by telling the program to only look at item 1, which is actually item 2)
                try:
                    for item in citypage_county_listinfo[1] :

                        # the "items" the previous line of code produces includes a bunch of null/empty items. We ignore those by just telling python to look at items that have "<li>" in them somewhere
                        if "<li>" in str(item) :

                            # makes sure the item is a string so it can be searched by regex
                            item_string = str(item)

                            # finds all county names and cleans up the regex result
                            county_name_raw = str(re.findall(r"(?<=信息\">).*?(?=<)", item_string))
                            county_name = regexcleaner(county_name_raw)

                            # finds all info for first person listed per county. This is a necessary first step in harvesting person1's information, as the way the html is written it would be impossible to pull person1 and person2's names separately just by using regex, so we have to break it up into person1 and person2 items, then parse those separately
                            county_person1_allinfo = str(re.findall(r"(?<=<em>).*?(?=</em>)", item_string))
                            # uses regex to search the variable we just created, then uses function defined at top to clean up the regex result
                            county_person1_name_raw = str(re.findall(r"(?<=htm\">).*?(?=</a>)", county_person1_allinfo))
                            county_person1_name = regexcleaner(county_person1_name_raw)
                            county_person1_url_raw = str(re.findall(r"(?<=href=\").*?(?=\">)", county_person1_allinfo))
                            county_person1_url_cleaned = regexcleaner(county_person1_url_raw)
                            #makes url complete by adding prefix (internet archive will change date in url to load to last time page was scraped, so we chose a date at end of 2018 to ensure it was post-scraping)
                            county_person1_url = 'https://web.archive.org/web/20181226105432/http://ldzl.people.com.cn:80/dfzlk/front/' + county_person1_url_cleaned

                            # similar to the variable above, just finds all the info for the second person listed per county
                            county_person2_allinfo = str(re.findall(r"(?<=<i>).*?(?=</i>)", item_string))
                            county_person2_name_raw = str(re.findall(r"(?<=htm\">).*?(?=</a>)", county_person2_allinfo))
                            county_person2_name = regexcleaner(county_person2_name_raw)
                            county_person2_url_raw = str(re.findall(r"(?<=href=\").*?(?=\">)", county_person2_allinfo))
                            county_person2_url_cleaned = regexcleaner(county_person2_url_raw)
                            county_person2_url = 'https://web.archive.org/web/20181226105432/http://ldzl.people.com.cn:80/dfzlk/front/' + county_person2_url_cleaned

                            # since we'll have to nest dictionaries, this creates a temporary (nested) dictionary for each iteration of the loop
                            county_holder_dict = {}
                            county_holder_dict["person1"] = county_person1_name
                            county_holder_dict["url1"] = county_person1_url

                            # At the county level, there's only ever 2 people listed. so the pool will always be 2, and we can just pre-define that variable rather than having python do any fancy math
                            county_holder_dict["pool1"] = 2

                            # because of the way we had to separately pull and name each person's information, we know that the first person will always be ranked 1 and the second person ranked 2. So again, we don't need to do any math here, we can just pre-define these variables
                            county_holder_dict["rank1"] = 1
                            county_holder_dict["person2"] = county_person2_name
                            county_holder_dict["url2"] = county_person2_url
                            county_holder_dict["pool2"] = 2
                            county_holder_dict["rank2"] = 2
                            county_holder_dict["province"] = province_name
                            county_holder_dict["city"] = city_name
                            county_holder_dict["county"] = county_name

                            # this creates the big dictionary, that matches each person's name with their temporary dictionary information
                            county_dict[county_name] = county_holder_dict

                            print("E. " + province_name + " " + city_name + " " + county_name + " county person list generated")
                            print("")
                            #pprint(county_dict)

                    # then here we append each citys dictionary to the dictionary for all cities, so that we end up with one big list of city-level officials, rather than the last city scraped overwriting everything.
                    all_county_officials_dictlist.append(county_dict)

                # error handling -- shows you what city to go to to find the county that isn't scraping correctly.
                except Exception as e:
                    print (province_name + ' ' + city_name + ' Error:', e)
                    # still need to create something to print the error to the csv
                    county_holder_dict = {}
                    county_holder_dict["person1"] = 'none'
                    county_holder_dict["url1"] = 'none'

                    # At the county level, there's only ever 2 people listed. so the pool will always be 2, and we can just pre-define that variable rather than having python do any fancy math
                    county_holder_dict["pool1"] = 'none'

                    # because of the way we had to separately pull and name each person's information, we know that the first person will always be ranked 1 and the second person ranked 2. So again, we don't need to do any math here, we can just pre-define these variables
                    county_holder_dict["rank1"] = 'none'
                    county_holder_dict["person2"] = 'none'
                    county_holder_dict["url2"] = 'none'
                    county_holder_dict["pool2"] = 'none'
                    county_holder_dict["rank2"] = 'none'
                    county_holder_dict["province"] = province_name
                    county_holder_dict["city"] = city_name
                    county_holder_dict["county"] = 'unknown'

                    # this creates the big dictionary, that matches each person's name with their temporary dictionary information
                    county_dict[county_name] = county_holder_dict

                    print("E. " + province_name + " " + city_name + " " + county_name + " county person list generated WITH ERRORS")
                    print("")
                    print("")

                    # then here we append each citys dictionary to the dictionary for all cities, so that we end up with one big list of city-level officials, rather than the last city scraped overwriting everything.
                    all_county_officials_dictlist.append(county_dict)
                    #pass

                #pprint(county_dict)
                #print("")

                ##############################################################
                #take the line below out when you're running this for real
                citycounter += 1

#pprint(all_county_officials_dictlist)

'''
def title_list_function():
    # this gets the person's job title(s) and rank_indiv (which is the relative ranking of each person's titles, based on the order in which they appear)
    # it just finds the first instance of this thing because it appears twice on the page
    try:
        for entry in soup.find("span", {"class": "red2"}):
            #breaks up the titles if there are multiple titles for the one peson
            if '，' in entry:
                title_split_temp = entry.split('，')
                if '、' in title_split_temp:
                    title_split = title_split_temp.split('、').split('、')
            elif '、' in entry:
                title_split = entry.split('、')
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
'''



###################################################################################################
######### SCRAPING PROVINCIAL-LEVEL OFFICIALS' BIOS AND WRITING THEM TO CSV #######################
###################################################################################################


province_counter = 1
PersonID_counter = 1

# to iterate over a list of dictionaries, see last answer here: https://stackoverflow.com/questions/35864007/python-3-5-iterate-through-a-list-of-dictionaries
for province_officials_dict in all_prov_officials_dictlist:

    ##############################################################
    #take out this counter line when running for real
    if province_counter < 3 :
        ##############################################################
        #take the line below out when you're running this for real
        province_counter += 1
        provperson_counter = 1

        for province_official_name, holder_dict in province_officials_dict.items() :
            ##############################################################
            #take out this counter line when running for real
            if provperson_counter < 5 :

                page = requests.get(holder_dict["url"])
                soup = BeautifulSoup(page.text, 'lxml')

                ##############################################################
                #take the line below out when you're running this for real
                provperson_counter += 1

                # creates a list where we can add all the information about each official to get converted/printed to a csv
                prov_official_csv_holder = []

                Prov = holder_dict["province"]
                City = holder_dict["city"]
                County = holder_dict["county"]
                URL = holder_dict["url"]

                print(URL)


                # error handling for pages that weren't archived
                unarchived_page = soup.find('div', {'class': 'errorBorder'})
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

                # for everything that was archived
                else :

                    name = name_function()
                    print(name)

                    #title_list = title_list_function()
                    #print(title_list)

                    try:
                        for entry in soup.find("span", {"class": "red2"}):
                            #breaks up the titles if there are multiple titles for the one peson
                            if '，' in entry:
                                title_split_temp = entry.split('，')
                                if '、' in title_split_temp:
                                    title_split = title_split_temp.split('、').split('、')
                            elif '、' in entry:
                                title_split = entry.split('、')
                            else:
                                title_split = [entry]
                            #adds the titles to a list of dictionaries for writing later
                            #this list of dics will have title:rank_indiv
                            title_list = {}
                            for item in title_split:
                                title_list[(title_split.index(item))] = item
                            print(title_list)
                    except Exception as e:
                        print ('Error:', e)
                        title_list['Error'] = e
                        pass

                    # this breaks the title_list into discrete titles (still in order) for writing to the csv later
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


                    gender = gender_function()

                    ethnicity = ethnicity_function()

                    dob_year = dob_year_function()

                    dob_month = dob_month_function()

                    birth_province = birth_province_function()

                    birth_place = birth_place_function()

                    education = education_function()

                    date_archived = date_archived_function()

                    date_scraped = date_scraped_function()

                    PersonID = personID_function()

                    img_url = img_url_function()

                    url_save_file_name = url_save_file_name_function()

                    full_person_resume = resume_function()



                # DataFrame explanation: https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
                # indicates that each row of the pandas DataFrame will consist of these items, as we defined them above
                row_holder = [Prov, City, County, name, title_1, title_2, title_3, title_4, gender, ethnicity, dob_year, dob_month, birth_province, birth_place, education, date_archived, date_scraped, img_url, url_save_file_name, full_person_resume, URL]

                # adds the row we just created to the holder file we created at top
                prov_official_csv_holder.append(row_holder)

                # converts the row info into a DataFrame, defines the column and row headings
                prov_official_row = pd.DataFrame(prov_official_csv_holder, index=[PersonID], columns=['Province', 'City', 'County', 'Name','Title 1', 'Title 2', 'Title 3', 'Title 4', 'Gender', 'Ethnicity', 'Birth Year', 'Birth Month', "Birth Province", "Birth Place", "Education", "Archived", "Scraped", "Image URL", "Image Filename", "Resume", "URL"])


                # TODO ONCE THIS IS ON THE BIG PAGE, MAKE SURE THAT THE PROVINCE/COUNTY/ETC GET WRITTEN INTO CSV

                # writes that DF info to a csv and encodes it so we can read the csv
                # how to append to csv, and check first if there's already a header https://stackoverflow.com/questions/30991541/pandas-write-csv-append-vs-write/30991707
                with open('new.csv', 'a') as f:
                    prov_official_row.to_csv(f, mode='a', header=f.tell()==0, encoding='utf-8')

                #prov_official_row.to_csv('new.csv', mode='a', header=f.tell()==0, encoding='utf-8')

                PersonID_counter +=1

                print("one provincial-level official's data scraped")
                print("")



###################################################################################################
######### SCRAPING CITY-LEVEL OFFICIALS' BIOS AND WRITING THEM TO CSV #######################
###################################################################################################


cityofficial_counter = 1


# to iterate over a list of dictionaries, see last answer here: https://stackoverflow.com/questions/35864007/python-3-5-iterate-through-a-list-of-dictionaries
for citypage_officials_dict in all_city_officials_dictlist:

    ##############################################################
    #take out this counter line when running for real
    if cityofficial_counter < 5 :
        ##############################################################
        #take the line below out when you're running this for real
        cityofficial_counter += 1
        cityperson_counter = 1



        for citypage_nameonly_cleaned, city_holder_dict in citypage_officials_dict.items() :
            ##############################################################
            #take out this counter line when running for real
            if cityperson_counter < 5 :

                page = requests.get(city_holder_dict["url"])
                soup = BeautifulSoup(page.text, 'lxml')

                ##############################################################
                #take the line below out when you're running this for real
                cityperson_counter += 1

                # creates a list where we can add all the information about each official to get converted/printed to a csv
                city_official_csv_holder = []

                Prov = city_holder_dict["province"]
                City = city_holder_dict["city"]
                County = city_holder_dict["county"]
                URL = city_holder_dict["url"]

                print(URL)


                # error handling for pages that weren't archived
                unarchived_page = soup.find('div', {'class': 'errorBorder'})
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

                # for everything that was archived
                else :

                    name = name_function()
                    print(name)

                    #title_list = title_list_function()
                    #print(title_list)

                    try:
                        for entry in soup.find("span", {"class": "red2"}):
                            #breaks up the titles if there are multiple titles for the one peson
                            if '，' in entry:
                                title_split_temp = entry.split('，')
                                if '、' in title_split_temp:
                                    title_split = title_split_temp.split('、').split('、')
                            elif '、' in entry:
                                title_split = entry.split('、')
                            else:
                                title_split = [entry]
                            #adds the titles to a list of dictionaries for writing later
                            #this list of dics will have title:rank_indiv
                            title_list = {}
                            for item in title_split:
                                title_list[(title_split.index(item))] = item
                            print(title_list)
                    except Exception as e:
                        print ('Error:', e)
                        title_list['Error'] = e
                        pass

                    # this breaks the title_list into discrete titles (still in order) for writing to the csv later
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


                    gender = gender_function()

                    ethnicity = ethnicity_function()

                    dob_year = dob_year_function()

                    dob_month = dob_month_function()

                    birth_province = birth_province_function()

                    birth_place = birth_place_function()

                    education = education_function()

                    date_archived = date_archived_function()

                    date_scraped = date_scraped_function()

                    PersonID = personID_function()

                    img_url = img_url_function()

                    url_save_file_name = url_save_file_name_function()

                    full_person_resume = resume_function()


                # DataFrame explanation: https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
                # indicates that each row of the pandas DataFrame will consist of these items, as we defined them above
                row_holder = [Prov, City, County, name, title_1, title_2, title_3, title_4, gender, ethnicity, dob_year, dob_month, birth_province, birth_place, education, date_archived, date_scraped, img_url, url_save_file_name, full_person_resume, URL]

                # adds the row we just created to the holder file we created at top
                prov_official_csv_holder.append(row_holder)

                # converts the row info into a DataFrame, defines the column and row headings
                prov_official_row = pd.DataFrame(prov_official_csv_holder, index=[PersonID], columns=['Province', 'City', 'County', 'Name','Title 1', 'Title 2', 'Title 3', 'Title 4', 'Gender', 'Ethnicity', 'Birth Year', 'Birth Month', "Birth Province", "Birth Place", "Education", "Archived", "Scraped", "Image URL", "Image Filename", "Resume", "URL"])


                # TODO ONCE THIS IS ON THE BIG PAGE, MAKE SURE THAT THE PROVINCE/COUNTY/ETC GET WRITTEN INTO CSV

                # writes that DF info to a csv and encodes it so we can read the csv
                # how to append to csv, and check first if there's already a header https://stackoverflow.com/questions/30991541/pandas-write-csv-append-vs-write/30991707
                with open('new.csv', 'a') as f:
                    prov_official_row.to_csv(f, mode='a', header=f.tell()==0, encoding='utf-8')

                #prov_official_row.to_csv('new.csv', mode='a', header=f.tell()==0, encoding='utf-8')

                PersonID_counter +=1



                print("one city-level official's data scraped")
                print("")


'''

###################################################################################################
######### SCRAPING COUNTY-LEVEL OFFICIALS' BIOS AND WRITING THEM TO CSV #######################
###################################################################################################


countyofficial_counter = 1


# to iterate over a list of dictionaries, see last answer here: https://stackoverflow.com/questions/35864007/python-3-5-iterate-through-a-list-of-dictionaries
for county_dict in all_county_officials_dictlist:

    ##############################################################
    #take out this counter line when running for real
    if countyofficial_counter < 5 :
        ##############################################################
        #take the line below out when you're running this for real
        countyofficial_counter += 1
        countyperson_counter = 1



        for county_name, county_holder_dict in county_dict.items() :
            ##############################################################
            #take out this counter line when running for real
            if countyperson_counter < 5 :

                page = requests.get(county_holder_dict["url"])
                soup = BeautifulSoup(page.text, 'lxml')




                ##############################################################
                #take the line below out when you're running this for real
                countyperson_counter += 1

                # creates a list where we can add all the information about each official to get converted/printed to a csv
                county_official_csv_holder = []

                Prov = county_holder_dict["province"]
                City = county_holder_dict["city"]
                County = county_holder_dict["county"]
                URL = county_holder_dict["url"]

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
                    title_list['Error'] = e
                    pass

                # this breaks the title_list into discrete titles (still in order) for writing to the csv later
                number_of_titles = len(title_list)
                if number_of_titles == 1 :
                    title_1 = title_list[1]
                    title_2 = ("")
                    title_3 = ("")
                    title_4 = ("")
                elif number_of_titles == 2 :
                    title_1 = title_list[1]
                    title_2 = title_list[2]
                    title_3 = ("")
                    title_4 = ("")
                elif number_of_titles == 3 :
                    title_1 = title_list[1]
                    title_2 = title_list[2]
                    title_3 = title_list[3]
                    title_4 = ("")
                elif number_of_titles == 4 :
                    title_1 = title_list[1]
                    title_2 = title_list[2]
                    title_3 = title_list[3]
                    title_4 = title_list[4]
                else :
                    pass

                # this is the gender section
                try:
                    gender = soup.find('p').contents[1]
                    # print(gender)
                except Exception as e:
                    print ('Error:', e)
                    gender = 'Error:', e
                    pass

                # this is the ethnicity section
                try:
                    ethnicity_unparsed = str(soup.find('div', {'class': 'p2j_text'}).contents[1])
                    eth_cut = ethnicity_unparsed.split('，')
                    ethnicity = eth_cut[2]
                    # print(ethnicity)
                except Exception as e:
                    print ('Error:', e)
                    ethnicity = 'Error:', e
                    pass

                #this is the dob section
                try:
                    dob_unparsed = soup.find('p').contents[5]
                    dob_year = dob_unparsed[0:4]
                    # print(dob_year)
                    dob_month = dob_unparsed[5:7]
                    # print(dob_month)
                except Exception as e:
                    print ('Error:', e)
                    dob_year = 'Error:', e
                    dob_month = 'Error:', e
                    pass

                # this is the birth_province and birth_place section
                try:
                    birth_location_unparsed = soup.find('p').contents[9]
                    birth_province = birth_location_unparsed[0:2]
                    # print(birth_province)
                    birth_place = birth_location_unparsed[2:4]
                    # print(birth_place)
                except Exception as e:
                    print ('Error:', e)
                    birth_province = 'Error:', e
                    birth_place = 'Error:', e
                    pass

                # this is the education section
                try:
                    education = soup.find('p').contents[13]
                    #print(education)
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
                    #print(date_archived)
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
                    #print(date_scraped)
                except Exception as e:
                    print ('Error:', e)
                    date_scraped = 'Error:', e
                    pass

                if len(str(CountyPersonID_counter)) == 1 :
                    PersonID = '0000000' + str(CountyPersonID_counter)
                elif len(str(CountyPersonID_counter)) == 2 :
                    PersonID = '000000' + str(CountyPersonID_counter)
                elif len(str(CountyPersonID_counter)) == 3 :
                    PersonID = '00000' + str(CountyPersonID_counter)
                elif len(str(CountyPersonID_counter)) == 4 :
                    PersonID = '0000' + str(CountyPersonID_counter)
                elif len(str(CountyPersonID_counter)) == 5 :
                    PersonID = '000' + str(CountyPersonID_counter)
                elif len(str(CountyPersonID_counter)) == 6 :
                    PersonID = '00' + str(CountyPersonID_counter)
                elif len(str(CountyPersonID_counter)) == 7 :
                    PersonID = '0' + str(CountyPersonID_counter)
                else :
                    PersonID = CountyPersonID_counter
                #PersonID = CountyPersonID_counter

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
                    #print(img_url)
                except Exception as e:
                    print ('Error:', e)
                    img_url = 'Error:', e
                    pass

                # this names and saves the image file
                try:
                    #I assume this will be a dynamically created variable
                    url_save_file_name = 'photo_' + str(PersonID) + '.jpg'

                    url_save_file_path = 'images/' + url_save_file_name
                    #uses requests to download the picture
                    image_r = requests.get(img_url, allow_redirects=True)
                    #writes the downloaded picture to the file
                    open(url_save_file_path, 'wb').write(image_r.content)
                    #print(url_save_file_name + " saved")
                except Exception as e:
                    print ('Error:', e)
                    url_save_file_name = 'Error:', e
                    pass

                #this is the person's CV as listed at the bottom of the page, pulled in full then cleaned up to strip out unnecessary characters/tags
                try:
                    data_dump = str(soup.find('div', {'class', 'p2j_text'}))
                    full_person_resume = str((re.sub("<p>|</p>|<div class=\"p2j_text\">|</div>", "", data_dump)))
                    #print(full_person_resume)
                except Exception as e:
                    print ('Error:', e)
                    full_person_resume = 'Error:', e
                    pass

                # DataFrame explanation: https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
                # indicates that each row of the pandas DataFrame will consist of these items, as we defined them above
                row_holder = [Prov, City, County, name, title_1, title_2, title_3, title_4, gender, ethnicity, dob_year, dob_month, birth_province, birth_place, education, date_archived, date_scraped, img_url, url_save_file_name, full_person_resume, URL]

                # adds the row we just created to the holder file we created at top
                county_official_csv_holder.append(row_holder)

                # converts the row info into a DataFrame, defines the column and row headings
                county_official_row = pd.DataFrame(county_official_csv_holder, index=[PersonID], columns=['Province', 'City', 'County', 'Name','Title 1', 'Title 2', 'Title 3', 'Title 4', 'Gender', 'Ethnicity', 'Birth Year', 'Birth Month', "Birth Province", "Birth Place", "Education", "Archived", "Scraped", "Image URL", "Image Filename", "Resume", "URL"])


                # TODO ONCE THIS IS ON THE BIG PAGE, MAKE SURE THAT THE PROVINCE/COUNTY/ETC GET WRITTEN INTO CSV

                # writes that DF info to a csv and encodes it so we can read the csv
                # how to append to csv, and check first if there's already a header https://stackoverflow.com/questions/30991541/pandas-write-csv-append-vs-write/30991707
                with open('new.csv', 'a') as f:
                    county_official_row.to_csv(f, mode='a', header=f.tell()==0, encoding='utf-8')

                #prov_official_row.to_csv('new.csv', mode='a', header=f.tell()==0, encoding='utf-8')

                PersonID_counter +=1



                print("one county-level official's data scraped")
                print("")

'''

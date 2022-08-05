def warn(*args, **kwargs):
    pass
import sys
import warnings
warnings.warn = warn
import time
from config import driver_setup , error_log
import re
import os
import csv
from datetime import datetime
import wx
app = wx.App()
class LyricsThings:
    def __init__(self) -> None:
        self.load_more = '//div[contains(@class,"Charts__LoadMore")]/div'
        self.click_filter = '//div[starts-with(@class,"SquareSelectTitle__Container")]'

        self.songs = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[1]/div[2]/div[1]'
        self.songs_day = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[3]/div[2]/div[1]'
        self.songs_week = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[3]/div[3]/div[1]'
        self.songs_month = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[3]/div[4]/div[1]'
        self.songs_alltime = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[3]/div[5]/div[1]'

        self.albums = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[1]/div[3]/div[1]'
        self.albums_day = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[2]/div[2]/div[1]'
        self.albums_week = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[2]/div[3]/div[1]'
        self.albums_month = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[2]/div[4]/div[1]'
        self.albums_alltime = '//div[starts-with(@class,"SquareManySelects__Selects")]/div[2]/div[5]/div[1]'

        self.song_info = '//div[starts-with(@class,"SongInfo__Columns")]'
        self.song_tags = '//div[starts-with(@class,"SongTags__Container")]/a'

        self.lyrics = '//div[starts-with(@class,"Lyrics__Container")]'

        self.main_filter = ["songs", "Albums"]
        self.base_filter = ["Day", "Week", "Month", "All Time"]

        self.selected_main_filter = None
        self.selected_base_filter = None

        self.regex = re.compile('[a-zA-Z@_!#$%^&*()<>?/\|}{~:]')

        self.error_message1 = "\n *** Please Enter Valid Number *** \n"
        self.error_message2 = "\n *** Please Enter Number Without Any Letters or Special Character  *** \n"
        self.error_message3 = "\n *** Chromedriver Error Found Please Read REDME FILE For Configuration *** \n"
        self.error_message4 = "\n *** Some Errors Found Please Give It Back To Maintenance *** \n"
        self.error_message5 = "\n *** Please Close Opened CSV Sheet An Try It Again OR Restart Application *** \n"
        self.error_message6 = "\n *** Taking Longer Time To Load URL Please Restart Application *** \n"
        self.browser = driver_setup()
        self.headers = ["Date","Title","Categories", "Lyrics","Tag"]

    def sent_error_message(self, message):
        print(message)
        wx.MessageBox(message.replace("\n",""), 'Error', wx.OK | wx.ICON_ERROR)

    def userinput(self):
        input_text = ''
        for count, filter_type in enumerate(self.main_filter):
            input_text += f'{count} => {filter_type.capitalize()}\n'
        while True:
            number = input(f'{input_text}\nSelect Category (NUMBER): ')
            if(self.regex.search(number) == None):
                self.selected_main_filter = int(number.strip())
                if len(self.main_filter) > self.selected_main_filter:
                    print(self.selected_main_filter)
                    print("="*28)
                    print(f"You Selected : {self.main_filter[self.selected_main_filter]}")
                    print("="*28)
                    break
                else:
                    self.sent_error_message(self.error_message1)
            else:
                self.sent_error_message(self.error_message2)

        input_text = ''
        for count, filter_type in enumerate(self.base_filter):
            input_text += f'{count} => {filter_type.capitalize()}\n'
        while True:
            number = input(f'{input_text}\nSelect Base Category (NUMBER): ')
            if(self.regex.search(number) == None):
                self.selected_base_filter = int(number.strip())
                if len(self.base_filter) > self.selected_base_filter:
                    print("="*28)
                    print(f"You Selected : {self.base_filter[self.selected_base_filter]}")
                    print("="*28)
                    break
                else:
                    self.sent_error_message(self.error_message1)
            else:
                self.sent_error_message(self.error_message2)
        self.browser.get("https://genius.com/")
        time.sleep(4)
        return self.main_filter[self.selected_main_filter]
    
    def clicking_things(self):
        print("\n***Filter Applying***")
        main_xpath = ''
        base_main_xpath = ''
        if self.main_filter[self.selected_main_filter] == "songs":
            main_xpath = self.songs
            if self.base_filter[self.selected_base_filter] == "Day":
                base_main_xpath = self.songs_day
            elif self.base_filter[self.selected_base_filter] == "Week":
                base_main_xpath = self.songs_week
            elif self.base_filter[self.selected_base_filter] == "Month":
                base_main_xpath = self.songs_month
            else:
                base_main_xpath = self.songs_alltime
        else:
            main_xpath = self.albums
            if self.base_filter[self.selected_base_filter] == "Day":
                base_main_xpath = self.albums_day
            elif self.base_filter[self.selected_base_filter] == "Week":
                base_main_xpath = self.albums_week
            elif self.base_filter[self.selected_base_filter] == "Month":
                base_main_xpath = self.albums_month
            else:
                base_main_xpath = self.albums_alltime
        
        while True:
            try:
                for click_filter_Tab in self.browser.find_elements_by_xpath(self.click_filter):
                    click_filter_Tab.click()
                    time.sleep(2)
                    break
                break
            except:
                print("Trying To click Filter Tab")
                time.sleep(2)
        while True:
            try:
                for click_filter in self.browser.find_elements_by_xpath(main_xpath):
                    click_filter.click()
                    time.sleep(2)
                    break
                break
            except:
                print("Trying To Select Main Filter")
                time.sleep(2)
        
        while True:
            try:
                for click_filter_Tab in self.browser.find_elements_by_xpath(self.click_filter):
                    click_filter_Tab.click()
                    time.sleep(2)
                    break
                break
            except:
                print("Trying To click Filter Tab")
                time.sleep(2)
    
        while True:
            try:
                for base_click_filter in self.browser.find_elements_by_xpath(base_main_xpath):
                    base_click_filter.click()
                    time.sleep(2)
                    break
                break
            except:
                print("Trying To Select Base Filter")
                time.sleep(2)
        print("\n***Pagination Working (LOAD MORE) It will take some time***")
        while True:
            try:
                found = False
                for loadmore in self.browser.find_elements_by_xpath(self.load_more):
                    loadmore.click()
                    time.sleep(4)
                    found = True
                    break
                if found == False:break
            except:
                print("Trying to load more")

    def songs_scrap(self):
        date = datetime.now().strftime("%Y-%m-%d-%H.%M")
        filename = f"./{date} {self.main_filter[self.selected_main_filter]} {self.base_filter[self.selected_base_filter]} Data.csv"
        with open(filename, mode='w',newline='',encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()
            total_links = []
            for link in self.browser.find_elements_by_xpath('//*[@id="top-songs"]/div/div[3]/a'):
                total_links.append(link.get_attribute("href"))
            for count, link in enumerate(total_links):
                while True:
                    try:
                        error = 0
                        while True:
                            try:
                                print(count, link," Navigating Link ....")
                                self.browser.get(link)
                                time.sleep(3)
                                break
                            except Exception as e:
                                if error == 4:
                                    error_log(e)
                                else:
                                    print(f"Retrying ... {link} ")
                                    time.sleep(3)
                                    error += 1
                        
                        title = ''
                        for song_title in self.browser.find_elements_by_xpath('//span[starts-with(@class,"SongHeaderdesktop__HiddenMask")]'):
                            title = f'{song_title.get_attribute("innerText").strip().capitalize()} Lyrics'
                            break
                        # print("Title: ",title)
                        
                        released_date = ''
                        artist = ""
                        for data in self.browser.find_elements_by_xpath('//div[starts-with(@class,"HeaderMetadata__Section")]'):
                            type = data.get_attribute("innerText").strip()
                            if "Produced by" in type:
                                artist = re.sub('\s+', ' ', type)
                                if "more" in artist:
                                    artist = artist.partition(",")[0]
                                title += f' - {artist.replace("Produced by","").replace("&",",")}'
                                # print("artist: ",type)
                                
                            elif "Release Date" in type:
                                released_date = re.sub('\s+', ' ', type).replace("Release Date","").replace("&",",")
                                # print("Released_date: ",released_date)

                        info = ''
                        for song_info in self.browser.find_elements_by_xpath(self.song_info):
                            main = song_info.get_attribute("innerText").replace('©','').replace('℗','').strip()
                            info_list = main.split("\n")
                            while len(info_list) != 0:
                                try:
                                    if "Samples" not in info_list[0] or "Covers" not in info_list[0] or "Remixes" not in info_list[0] or "Release Date" not in info_list[0]:
                                        
                                        if len(info_list[0]) <= 20:
                                            if len(info_list[1].strip()) > 150:
                                                info_list[1] = f'{info_list[1][:150].strip()}...'
                                            info += f"{info_list[0].strip()}:{info_list[1]}<BR>"
                                    # print(info_list[0],":",info_list[1])
                                    del info_list[0]
                                    del info_list[0]
                                except IndexError:
                                    # error_log("Index Error")
                                    print("Index Error")
                            break
                        info = info.rstrip("<BR>")
                        # print("Song Info: ",info)

                        lyrics = ''
                        for song_lyrics in self.browser.find_elements_by_xpath('//div[@class="Lyrics__Container-sc-1ynbvzw-6 YYrds"]'):
                            lyrics += f"{title} <BR><BR><BR>"
                            lyrics += song_lyrics.get_attribute("innerText").strip().replace('\n',"<BR>").replace("<BR><BR>",'<BR>')
                            lyrics += f"<BR><BR><BR><BR>{info}"
                            break
                        
                        # print("Song lyrics: ",lyrics)

                        tag = ''
                        tag += title + ','
                        for song_tag in self.browser.find_elements_by_xpath(self.song_tags):
                            tag += song_tag.get_attribute("innerText").strip() + ','
                        tag = tag.rstrip(',')
                        # print("Song Tag: ",tag)
                        if re.match("^[\W A-Za-z0-9_@?./#&+-]*$", lyrics+tag):
                            detail_dic = {
                                    self.headers[0] : released_date,
                                    self.headers[1] : title,
                                    self.headers[2] : "English Lyrics",
                                    self.headers[3] : lyrics.replace('©','').replace('℗','').strip(),
                                    self.headers[4] : tag
                                }
                            writer.writerow(detail_dic)
                        break
                    except Exception as e:
                        error_log(e)
                        print(f"Retrying ... {link} ")
                        time.sleep(2)

    def album_scrap(self):
        while True:
            try:
                total_albums = []
                for link in self.browser.find_elements_by_xpath('//*[@id="top-songs"]/div/div[3]/a'):
                    total_albums.append(link.get_attribute("href"))
                break
            except Exception as e:
                print(f"Retrying ... {link} ")
                time.sleep(3)
        
        total_links = []
        for count, album_link in enumerate(total_albums):
            while True:
                try:
                    error = 0
                    while True:
                        try:
                            print("="*50)
                            print(count,album_link,"Navigating Link ....")
                            self.browser.get(album_link)
                            time.sleep(3)
                            break
                        except Exception as e:
                            print(f"Retrying ... {album_link} ")
                            time.sleep(3)
                    self.browser.get(album_link)
                    time.sleep(2)
                    count = 0
                    for link in self.browser.find_elements_by_xpath('//album-tracklist-row[@album-appearance="album_appearance"]/div[1]/div[2]/a'):
                        total_links.append(link.get_attribute("href"))
                        count += 1
                    print(count, "Lyrics link found from album")
                    break
                except Exception as e:
                    error_log(e)
                    print(f"Retrying ... {link} ")
                    time.sleep(2)
        
        date = datetime.now().strftime("%Y-%m-%d-%H.%M")
        filename = f"./{date} {self.main_filter[self.selected_main_filter]} {self.base_filter[self.selected_base_filter]} Data.csv"
        with open(filename, mode='w',newline='',encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()
            for count, link in enumerate(total_links):
                while True:
                    try:
                        error = 0
                        while True:
                            try:
                                print(count, link," Navigating Link ....")
                                self.browser.get(link)
                                time.sleep(3)
                                break
                            except Exception as e:
                                if error == 4:
                                    error_log(e)
                                else:
                                    print(f"Retrying ... {link} ")
                                    time.sleep(3)
                                    error += 1
                        
                        title = ''
                        for song_title in self.browser.find_elements_by_xpath('//span[starts-with(@class,"SongHeaderdesktop__HiddenMask")]'):
                            title = f'{song_title.get_attribute("innerText").strip().capitalize()} Lyrics'
                            break
                        # print("Title: ",title)
                        
                        released_date = ''
                        artist = ""
                        for data in self.browser.find_elements_by_xpath('//div[starts-with(@class,"HeaderMetadata__Section")]'):
                            type = data.get_attribute("innerText").strip()
                            if "Produced by" in type:
                                artist = re.sub('\s+', ' ', type)
                                if "more" in artist:
                                    artist = artist.partition(",")[0]
                                title += f' - {artist.replace("Produced by","").replace("&",",")}'
                                # print("artist: ",type)
                                
                            elif "Release Date" in type:
                                released_date = re.sub('\s+', ' ', type).replace("Release Date","").replace("&",",")
                                # print("Released_date: ",released_date)

                        info = ''
                        for song_info in self.browser.find_elements_by_xpath(self.song_info):
                            main = song_info.get_attribute("innerText").replace('©','').replace('℗','').strip()
                            info_list = main.split("\n")
                            while len(info_list) != 0:
                                try:
                                    if "Samples" not in info_list[0] or "Covers" not in info_list[0] or "Remixes" not in info_list[0] or "Release Date" not in info_list[0]:
                                        
                                        if len(info_list[0]) <= 20:
                                            if len(info_list[1].strip()) > 150:
                                                info_list[1] = f'{info_list[1][:150].strip()}...'
                                            info += f"{info_list[0].strip()}:{info_list[1]}<BR>"
                                    # print(info_list[0],":",info_list[1])
                                    del info_list[0]
                                    del info_list[0]
                                except IndexError:
                                    # error_log("Index Error")
                                    print("Index Error")
                            break
                        info = info.rstrip("<BR>")
                        # print("Song Info: ",info)

                        lyrics = ''
                        for song_lyrics in self.browser.find_elements_by_xpath('//div[@class="Lyrics__Container-sc-1ynbvzw-6 YYrds"]'):
                            lyrics += f"{title} <BR><BR><BR>"
                            lyrics += song_lyrics.get_attribute("innerText").strip().replace('\n',"<BR>").replace("<BR><BR>",'<BR>')
                            lyrics += f"<BR><BR><BR><BR>{info}"
                            break
                        
                        # print("Song lyrics: ",lyrics)

                        tag = ''
                        tag += title + ','
                        for song_tag in self.browser.find_elements_by_xpath(self.song_tags):
                            tag += song_tag.get_attribute("innerText").strip() + ','
                        tag = tag.rstrip(',')
                        # print("Song Tag: ",tag)
                        if re.match("^[\W A-Za-z0-9_@?./#&+-]*$", lyrics+tag):
                            detail_dic = {
                                    self.headers[0] : released_date,
                                    self.headers[1] : title,
                                    self.headers[2] : "English Lyrics",
                                    self.headers[3] : lyrics.replace('©','').replace('℗','').strip(),
                                    self.headers[4] : tag
                                }
                            writer.writerow(detail_dic)
                        break
                    except Exception as e:
                        error_log(e)
                        print(f"Retrying ... {link} ")
                        time.sleep(2)

lyricsthings = LyricsThings()
filter_type = lyricsthings.userinput()
lyricsthings.clicking_things()
if filter_type == "songs":
    lyricsthings.songs_scrap()
else:
    lyricsthings.album_scrap()

wx.MessageBox("Data Mining Successfully Done", 'Success', wx.OK | wx.ICON_INFORMATION)
input('Please Enter To Exit')
quit()
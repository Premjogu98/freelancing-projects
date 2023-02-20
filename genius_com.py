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
from csv_to_xlsx import csv_to_xlsx
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
        if not self.browser:
            sys.exit()
        self.headers = ["Date","Title","Lyrics","Categories","Tag"]

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
            for link in self.browser.find_elements_by_xpath('//*[@id="top-songs"]/div/div[2]/a'):
                total_links.append(link.get_attribute("href"))
            # print(total_links)
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
                        
                        unrelease_message = ""
                        for message in self.browser.find_elements_by_xpath('//div[starts-with(@class,"LyricsPlaceholder__Message")]'):
                            unrelease_message = message.get_attribute("innerText").strip()
                            break
                        if "yet to be released" not in unrelease_message:
                            
                            artist = ""
                            title = ""
                            title_with_artist = ""
                            for song_title in self.browser.find_elements_by_xpath('//h1[starts-with(@class,"SongHeaderWithPrimis__Title")]/span'):
                                title_with_artist = title = f'{song_title.get_attribute("innerText").strip().capitalize()} Lyrics'
                                break
                            if not title:
                                for song_title in self.browser.find_elements_by_xpath('//h1[starts-with(@class,"SongHeaderdesktop__Title")]/span'):
                                    title_with_artist = title = f'{song_title.get_attribute("innerText").strip().capitalize()} Lyrics'
                                    break
                            # print("Title: ",title)
                            for song_artist in self.browser.find_elements_by_xpath('//div[starts-with(@class,"HeaderArtistAndTracklistPrimis")]/a'):
                                artist += song_artist.get_attribute("innerText").strip().capitalize()+' | '
                            if artist:
                                artist = artist.strip().rstrip("|").strip()
                                title_with_artist += f' - {artist}'
                            if not artist:
                                for song_artist in self.browser.find_elements_by_xpath('//a[contains(@class,"SongHeaderdesktop__Artist")]'):
                                    artist += song_artist.get_attribute("innerText").strip().capitalize()+' | '
                                if artist:
                                    artist = artist.strip().rstrip("|").strip()
                                    title_with_artist += f' - {artist}'
                            # print("artist: ",artist)
                            info = ''
                            album_text = ''
                            released_date = ''
                            for album in self.browser.find_elements_by_xpath('//div[contains(@class,"HeaderArtistAndTracklistPrimis__Tracklist")]/a'):
                                album_text = album.get_attribute("innerText").strip()
                                break
                            label_len = 0
                            try:
                                label_len = len(self.browser.find_elements_by_xpath('//div[starts-with(@class,"SongInfo__Columns")]/div'))
                            except Exception as e:
                                error_log(e)
                            for index in range(1,label_len+1,1):
                                for cred_label in self.browser.find_elements_by_xpath(f'//div[starts-with(@class,"SongInfo__Columns")]/div[{index}]/div[1]'):
                                    cred_label_text = cred_label.get_attribute("innerText").replace('©','').replace('℗','').strip()
                                    break
                                for cred_label_val in self.browser.find_elements_by_xpath(f'//div[starts-with(@class,"SongInfo__Columns")]/div[{index}]/div[2]'):
                                    cred_label_val_text = cred_label_val.get_attribute("innerText").strip()
                                    if "Release Date" in cred_label_text:
                                        released_date = cred_label_val_text
                                    break
                                if released_date:
                                    break
                            if album_text:
                                info += f"""<p style="margin: 5px;"><strong>Album</strong> - {album_text} By {artist}</p>"""
                            else:
                                info += f"""<p style="margin: 5px;"><strong>Album</strong> - {title.replace("Lyrics","").strip()} By {artist}</p>"""
                            if released_date:
                                info +=  f"""<p style="margin-top: 5px;"><strong>Release Date</strong> - {released_date}</p>"""
                                
                            # print("Song Info: ",info)

                            lyrics = ''
                            complete_lyrics = ""
                            for song_lyrics in self.browser.find_elements_by_xpath('//div[@class="Lyrics__Container-sc-1ynbvzw-6 YYrds"]'):
                                lyrics += song_lyrics.get_attribute("innerText").strip().replace('\n',"<BR>")

                            complete_lyrics += f'<h2 style="text-align: center;">{title_with_artist}</h2> <BR><BR><BR>'
                            complete_lyrics += f'<p style="text-align: center;">{lyrics}</p>'
                            complete_lyrics += f'<BR><BR><BR><BR><blockquote style="text-align: center;">{info}</blockquote>'
                            # print("Song lyrics: ",lyrics)
                            
                            tag = ''
                            tag += title + ','
                            for song_tag in self.browser.find_elements_by_xpath(self.song_tags):
                                tag += song_tag.get_attribute("innerText").strip() + ','
                            tag = tag.strip(',').rstrip(',')
                            # print("Song Tag: ",tag)
                            # if re.match("^[\W A-Za-z0-9_@?./#&+-]*$", lyrics+tag):
                            detail_dic = {
                                    self.headers[0] : released_date,
                                    self.headers[1] : title_with_artist,
                                    self.headers[2] : complete_lyrics.replace('©','').replace('℗','').strip(),
                                    self.headers[3] : "English Lyrics",
                                    self.headers[4] : tag
                                }
                            writer.writerow(detail_dic)
                        break
                    except Exception as e:
                        error_log(e)
                        print(f"Retrying ... {link} ")
                        time.sleep(2)
        
        print("\n\nFILE EXPORTING...........")
        if csv_to_xlsx(filename,filename.replace(".csv",".xlsx")):
            print(f"\nFILE EXPORTED: {filename.replace('.csv','.xlsx')}...........\n\n")
        else:
            print("\n\nFILE EXPORITNG FAILED !!!")
            wx.MessageBox("FILE EXPORITNG FAILED !!! >>> EXPECTED EXE MAINTEINANCE <<< ", 'ERROR', wx.OK | wx.ICON_ERROR)

        os.remove(filename)
        self.browser.quit()
    def album_scrap(self):
        while True:
            try:
                total_albums = []
                for link in self.browser.find_elements_by_xpath('//div[@id="top-songs"]/div/div[2]/a'):
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
                        unrelease_message = ""
                        for message in self.browser.find_elements_by_xpath('//div[starts-with(@class,"LyricsPlaceholder__Message")]'):
                            unrelease_message = message.get_attribute("innerText").strip()
                            break
                        if "yet to be released" not in unrelease_message:
                            
                            artist = ""
                            title = ""
                            title_with_artist = ""
                            for song_title in self.browser.find_elements_by_xpath('//h1[starts-with(@class,"SongHeaderWithPrimis__Title")]/span'):
                                title_with_artist = title = f'{song_title.get_attribute("innerText").strip().capitalize()} Lyrics'
                                break
                            if not title:
                                for song_title in self.browser.find_elements_by_xpath('//h1[starts-with(@class,"SongHeaderdesktop__Title")]/span'):
                                    title_with_artist = title = f'{song_title.get_attribute("innerText").strip().capitalize()} Lyrics'
                                    break
                            # print("Title: ",title)
                            for song_artist in self.browser.find_elements_by_xpath('//div[starts-with(@class,"HeaderArtistAndTracklistPrimis")]/a'):
                                artist += song_artist.get_attribute("innerText").strip().capitalize()+' | '
                            if artist:
                                artist = artist.strip().rstrip("|").strip()
                                title_with_artist += f' - {artist}'
                            if not artist:
                                for song_artist in self.browser.find_elements_by_xpath('//a[contains(@class,"SongHeaderdesktop__Artist")]'):
                                    artist += song_artist.get_attribute("innerText").strip().capitalize()+' | '
                                if artist:
                                    artist = artist.strip().rstrip("|").strip()
                                    title_with_artist += f' - {artist}'
                            # print("artist: ",artist)
                            info = ''
                            album_text = ''
                            released_date = ''
                            for album in self.browser.find_elements_by_xpath('//div[contains(@class,"HeaderArtistAndTracklistPrimis__Tracklist")]/a'):
                                album_text = album.get_attribute("innerText").strip()
                                break
                            label_len = 0
                            try:
                                label_len = len(self.browser.find_elements_by_xpath('//div[starts-with(@class,"SongInfo__Columns")]/div'))
                            except Exception as e:
                                error_log(e)
                            for index in range(1,label_len+1,1):
                                for cred_label in self.browser.find_elements_by_xpath(f'//div[starts-with(@class,"SongInfo__Columns")]/div[{index}]/div[1]'):
                                    cred_label_text = cred_label.get_attribute("innerText").replace('©','').replace('℗','').strip()
                                    break
                                for cred_label_val in self.browser.find_elements_by_xpath(f'//div[starts-with(@class,"SongInfo__Columns")]/div[{index}]/div[2]'):
                                    cred_label_val_text = cred_label_val.get_attribute("innerText").strip()
                                    if "Release Date" in cred_label_text:
                                        released_date = cred_label_val_text
                                    break
                                if released_date:
                                    break
                            if album_text:
                                info += f"""<p style="margin: 5px;"><strong>Album</strong> - {album_text} By {artist}</p>"""
                            else:
                                info += f"""<p style="margin: 5px;"><strong>Album</strong> - {title.replace("Lyrics","").strip()} By {artist}</p>"""
                            if released_date:
                                info +=  f"""<p style="margin-top: 5px;"><strong>Release Date</strong> - {released_date}</p>"""
                                
                            # print("Song Info: ",info)

                            lyrics = ''
                            complete_lyrics = ""
                            for song_lyrics in self.browser.find_elements_by_xpath('//div[@class="Lyrics__Container-sc-1ynbvzw-6 YYrds"]'):
                                lyrics += song_lyrics.get_attribute("innerText").strip().replace('\n',"<BR>")

                            complete_lyrics += f'<h2 style="text-align: center;">{title_with_artist}</h2> <BR><BR><BR>'
                            complete_lyrics += f'<p style="text-align: center;">{lyrics}</p>'
                            complete_lyrics += f'<BR><BR><BR><BR><blockquote style="text-align: center;">{info}</blockquote>'
                            # print("Song lyrics: ",lyrics)
                            
                            tag = ''
                            tag += title + ','
                            for song_tag in self.browser.find_elements_by_xpath(self.song_tags):
                                tag += song_tag.get_attribute("innerText").strip() + ','
                            tag = tag.strip(',').rstrip(',')
                            # print("Song Tag: ",tag)
                            # if re.match("^[\W A-Za-z0-9_@?./#&+-]*$", lyrics+tag):
                            detail_dic = {
                                    self.headers[0] : released_date,
                                    self.headers[1] : title_with_artist,
                                    self.headers[2] : complete_lyrics.replace('©','').replace('℗','').strip(),
                                    self.headers[3] : "English Lyrics",
                                    self.headers[4] : tag
                                }
                            writer.writerow(detail_dic)
                        break
                    except Exception as e:
                        error_log(e)
                        print(f"Retrying ... {link} ")
                        time.sleep(2)
        
        print("\n\nFILE EXPORTING...........")
        if csv_to_xlsx(filename,filename.replace(".csv",".xlsx")):
            print(f"\nFILE EXPORTED: {filename.replace('.csv','.xlsx')}...........\n\n")
        else:
            print("\n\nFILE EXPORITNG FAILED !!!")
            wx.MessageBox("FILE EXPORITNG FAILED !!! >>> EXPECTED EXE MAINTEINANCE <<< ", 'ERROR', wx.OK | wx.ICON_ERROR)

        os.remove(filename)
        self.browser.quit()
        
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
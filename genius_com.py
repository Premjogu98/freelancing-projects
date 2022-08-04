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
        self.load_more = '//div[@class="PageGridCenter-q0ues6-0 Charts__LoadMore-sc-1re0f44-1 eDwRUT"]/div'
        self.click_filter = '//div[@class="SquareSelectTitle__Container-sc-1vck5yn-0 euenQK"]'

        self.songs = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[1]/div[2]/div[1]'
        self.songs_day = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[3]/div[2]/div[1]'
        self.songs_week = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[3]/div[3]/div[1]'
        self.songs_month = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[3]/div[4]/div[1]'
        self.songs_alltime = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[3]/div[5]/div[1]'

        self.albums = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[1]/div[3]/div[1]'
        self.albums_day = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[2]/div[2]/div[1]'
        self.albums_week = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[2]/div[3]/div[1]'
        self.albums_month = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[2]/div[4]/div[1]'
        self.albums_alltime = '//div[@class="SquareManySelects__Selects-sc-1kktot3-4 hnIVtc"]/div[2]/div[5]/div[1]'

        self.song_info = '//div[@class="SongInfo__Columns-nekw6x-2 dWcYSx"]'
        self.song_tags = '//div[@class="SongTags__Container-xixwg3-1 bZsZHM"]/a'

        self.lyrics = '//div[@class="Lyrics__Container-sc-1ynbvzw-6 YYrds"]'

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

    def clicking_things(self):
        
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


lyricsthings = LyricsThings()
lyricsthings.userinput()
lyricsthings.clicking_things()
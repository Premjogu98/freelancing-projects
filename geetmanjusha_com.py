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
import string 
import wx
app = wx.App()

class LyricsThings:
    def __init__(self) -> None:
        
        self.error_message1 = "\n *** Please Enter Valid Number *** \n"
        self.error_message2 = "\n *** Please Enter Number Without Any Letters or Special Character  *** \n"
        self.error_message3 = "\n *** Chromedriver Error Found Please Read REDME FILE For Configuration *** \n"
        self.error_message4 = "\n *** Some Errors Found Please Give It Back To Maintenance *** \n"
        self.error_message5 = "\n *** Please Close Opened CSV Sheet An Try It Again OR Restart Application *** \n"
        self.error_message6 = "\n *** Taking Longer Time To Load URL Please Restart Application *** \n"
        self.browser = driver_setup()

        self.headers = ["Date","Title","Categories", "Lyrics","Tag"]

        self.regex = re.compile('[a-zA-Z@_!#$%^&*()<>?/\|}{~:]')

        self.main_filter = ["hindi", "marathi"]

        self.user_selected_option = None

    
    def sent_error_message(self, message):
        print(message)
        wx.MessageBox(message.replace("\n",""), 'Error', wx.OK | wx.ICON_ERROR)

    def user_input(self):
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

        # self.browser.get("https://geetmanjusha.com/")
        # time.sleep(4)

        self.user_selected_option = self.main_filter[self.selected_main_filter]

    def songs_scrap(self):

        for letter in string.ascii_uppercase:
            url = f"https://geetmanjusha.com/?option=com_pages&view=page&layout={self.user_selected_option}-index&indexstart={letter}"
            self.browser.get(url)
            time.sleep(2)
            if len(self.browser.find_elements_by_xpath('//div[@class="alert alert-info alert-block"]')) == 0:
                for link in self.browser.find_elements_by_xpath('//div[@class="an-entity an-record an-removable"]'):
                    html_data = re.sub(' +', ' ', link.get_attribute("outerHTML").strip())
                    # print(html_data)
                    a_tag_html = html_data.partition('<a ')[2].partition('/a>')[0]
                    lyrics_link , lyrics_tag = a_tag_html.partition('href="')[2].partition('"')[0].strip(), a_tag_html.partition('">')[2].partition('<')[0].strip().split("/")[1]
                    print(lyrics_link,"\n",lyrics_tag)
                    Lyricist = str(html_data.partition('entity-excerpt')[2].partition('</div>')[0]).split("/")[1]
                    print(Lyricist)
                    date = str(html_data.partition('entity-meta')[2].partition('</ul>')[0]).partition('Created')[2].partition('by')[0]
                    print(date)
                    # self.browser.get(link)
                    # time.sleep(2)
            else:
                print("No Lyrics Found")
        



lyricsthings = LyricsThings()
lyricsthings.user_input()
lyricsthings.songs_scrap()

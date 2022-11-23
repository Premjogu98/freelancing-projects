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
from openpyxl import Workbook


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

        self.collected_data = []
    
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

    def links_scrap(self):
        total_count = 1
        for count ,letter in enumerate(string.ascii_uppercase,start=1):
            url = f"https://geetmanjusha.com/?option=com_pages&view=page&layout={self.user_selected_option}-index&indexstart={letter}"
            self.browser.get(url)
            time.sleep(2)
            if len(self.browser.find_elements_by_xpath('//div[@class="alert alert-info alert-block"]')) == 0:
                for count1, link in enumerate(self.browser.find_elements_by_xpath('//div[@class="an-entity an-record an-removable"]')):
                    html_data = re.sub(' +', ' ', link.get_attribute("outerHTML").strip())

                    a_tag_html = html_data.partition('<a ')[2].partition('/a>')[0]
                    lyrics_link , lyrics_tag = html_data.partition('<a ')[2].partition('/a>')[0].partition('href="')[2].partition('"')[0].strip(), a_tag_html.partition('">')[2].partition('<')[0].strip().split("/")[0]
                    Lyricist = str(html_data.partition('entity-excerpt')[2].partition('</div>')[0]).split("/")[1].replace(",","<BR>")
                    date = str(html_data.partition('entity-meta')[2].partition('</ul>')[0]).partition('Created')[2].partition('by')[0]

                    self.collected_data.append({"alpha":letter, "link":lyrics_link, "lyrics_tag":lyrics_tag.title(), "song_detail": Lyricist.capitalize(), "date":date })
                    print(f"{count} --> {self.user_selected_option} --> {letter}  {total_count} {lyrics_link}")
                    total_count += 1
                break
            else:
                print("No Lyrics Found")

    def songs_scrap(self):
        book = Workbook()
        sheet = book.active

        sheet['A1'] = "Date"
        sheet['B1'] = "Title"
        sheet['C1'] = "Category"
        sheet['D1'] = "Lyrics"
        sheet['E1'] = "Tag"

        for count, data in enumerate(self.collected_data,start=3):
            print(f"{count} Link --> {data['link']}")
            self.browser.get(data["link"])
            time.sleep(2)
            lyrics_html = ""
            for lyrics in self.browser.find_elements_by_xpath('//div[@class="entity-description"][2]/pre'):
                lyrics_html = re.sub(' +', ' ', lyrics.get_attribute("outerHTML").strip().replace('<pre style="font-size:16px;">','').replace("</pre>",'').replace("\n\n","<BR>").replace("\n","<BR>"))
                print(lyrics_html)

            tags = f'{data["lyrics_tag"]} Lyrics'
        
            for tags_s in self.browser.find_elements_by_xpath('//a[@class="hashtag"]'):
                tags += tags_s.get_attribute("innerText").strip().replace("#","").title()+","
            for tags_s in data["song_detail"].split("<BR>"):
                tags += tags_s.partition(":")[2].strip()+","

            print(tags)
            break
            # sheet[f'A{count}'] = data["date"]
            # sheet[f'B{count}'] = f'{data["lyrics_tag"]} Lyrics'
            # sheet[f'C{count}'] = f'{self.user_selected_option} Lyrics'
            # sheet[f'D{count}'] = f'{data["lyrics_tag"]} Lyrics<BR><BR><BR>{lyrics_html}<BR><BR><BR><BR>{data["song_detail"]}'
            # sheet[f'E{count}'] = tags.rstrip(",")
            



lyricsthings = LyricsThings()
lyricsthings.user_input()
lyricsthings.links_scrap()
lyricsthings.songs_scrap()

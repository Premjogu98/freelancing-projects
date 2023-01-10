def warn(*args, **kwargs):
    pass
import sys
import warnings
warnings.warn = warn
import time
from config import driver_setup
import re
import os
import csv
from datetime import datetime
import string 
import wx
from csv_to_xlsx import csv_to_xlsx
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

        self.main_filter = ["hindi", "tamil", "telugu", "malayalam", "kannada", "punjabi"]

        self.user_selected_option = None

        self.collected_data = []
    
    def sent_error_message(self, message):
        print(message)
        wx.MessageBox(message.replace("\n",""), 'Error', wx.OK | wx.ICON_ERROR)

    def remove_html_text(self, string):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', string)
        return cleantext
        
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
        while True:
            print("***  Please Enter Page Number  ***")
            self.from_page = input(f'PAGE FROM : ').strip()
            self.to_page = input(f'PAGE TO : ').strip()
            if self.from_page != "" and self.to_page != "":
                if(self.regex.search(self.from_page) == None) and (self.regex.search(self.to_page) == None):
                    self.from_page = int(self.from_page)
                    self.to_page = int(self.to_page)
                    break
                else:
                    print(self.error_message2)
            else:
                print("\n***  Please Enter Page Number  ***\n")
        self.user_selected_option = self.main_filter[self.selected_main_filter]


    def songs_scrap(self):

        date = datetime.now().strftime("%Y-%m-%d-%H.%M")
        filename = f"./{date} {self.user_selected_option} Data.csv"
        with open(filename, mode='w',newline='',encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()
            # page = 1

            total_link = 1
            for page in range(self.from_page , self.to_page+1,1):
                self.browser.get(f"https://lyricsing.com/language/{self.user_selected_option}/page/{str(page)}")
                time.sleep(2)
                if len(self.browser.find_elements_by_xpath('//ul[@class="list-inline lyrics-block"]/li/div/a')) != 0:
                    urls = [{"link": lyrics_link.get_attribute("href"),"title":lyrics_link.get_attribute("title").strip()} for lyrics_link in self.browser.find_elements_by_xpath('//ul[@class="list-inline lyrics-block"]/li/div/a')]
                    for data in urls:
                        self.browser.get(data["link"])
                        time.sleep(2)
                        lyrics_tag = data["title"]

                        lyrics_html = ""
                        for lyrics in self.browser.find_elements_by_xpath('//div[@class="col-md-12 lyrics_content"]/p'):
                            lyrics_html += re.sub(' +', ' ', lyrics.get_attribute("outerHTML").strip().replace('<p>','').replace("Male : ",'').replace("Female : ",'').replace("</p>",'').replace("\n\n","<BR><BR>").replace("\n","<BR>"))
                        # print(lyrics_html)
                        
                        lyrics_details = ""
                        for lyrics_details_html in self.browser.find_elements_by_xpath('//div[@class="other_song_lyrics"]/table/tbody/tr'):
                            lyrics_details += f"""{self.remove_html_text(str(lyrics_details_html.get_attribute("outerHTML").split("</td>")[0]).partition('">')[2].strip())}:{self.remove_html_text(str(lyrics_details_html.get_attribute("outerHTML").split("</td>")[1]).partition('">')[2].strip())}<BR>"""
                            lyrics_tag += f""",{self.remove_html_text(str(lyrics_details_html.get_attribute("outerHTML").split("</td>")[1]).partition('">')[2].strip().replace(", ",','))}"""
                            
                        lyrics_details = lyrics_details.rstrip("<BR>")
                        # print(lyrics_details)

                        detail_dic = {
                            self.headers[0] : "",
                            self.headers[1] : f'{data["title"]}',
                            self.headers[2] : f'{self.user_selected_option} Lyrics',
                            self.headers[3] : f'{data["title"]}<BR><BR><BR>{lyrics_html}<BR><BR><BR><BR>{lyrics_details}',
                            self.headers[4] : lyrics_tag
                        }
                        writer.writerow(detail_dic)
                        print(f'PAGE {str(page)}/{str(self.to_page)} == Link {str(total_link)} --> {data["link"]}')
                        total_link += 1
                else:
                    print("NOTHING TO SCRAP")
                    break
        
        print("\n\nFILE EXPORTING...........")
        if csv_to_xlsx(filename,filename.replace(".csv",".xlsx")):
            print(f"\nFILE EXPORTED: {filename.replace('.csv','.xlsx')}\n")
        else:
            print("\n\nFILE EXPORITNG FAILED !!!")
            wx.MessageBox("FILE EXPORITNG FAILED !!! >>> EXPECTED EXE MAINTEINANCE <<< ", 'ERROR', wx.OK | wx.ICON_ERROR)

        os.remove(filename)
        self.browser.close()

lyricsthings = LyricsThings()
lyricsthings.user_input()
lyricsthings.songs_scrap()


wx.MessageBox(">>>>>  Data Mining Successfully Done  <<<<<", 'Success', wx.OK | wx.ICON_INFORMATION)
input('Please Enter To Exit')
import sys
sys.exit("Thank You ")
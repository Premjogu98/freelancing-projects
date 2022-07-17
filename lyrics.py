import time
from config import driver_setup , error_log
import re,os
import xlsxwriter
from datetime import datetime
import wx
app = wx.App()

class LyricsThings:

    def __init__(self):

        self.list_of_language = [
            "https://www.lyricsgaon.com/category/hindi-songs-lyrics/",
            "https://www.lyricsgaon.com/category/haryanvi-songs-lyrics/",
            "https://www.lyricsgaon.com/category/punjabi-songs-lyrics/",
            "https://www.lyricsgaon.com/category/bhojpuri-songs-lyrics/",
            "https://www.lyricsgaon.com/category/devotional-bhakti-songs-lyrics/"
        ]
        self.regex = re.compile('[a-zA-Z@_!#$%^&*()<>?/\|}{~:]')
        self.error_message1 = "\n *** Please Enter Valid Number *** \n"
        self.error_message2 = "\n *** Please Enter Number Without Any Letters or Special Character  *** \n"
        self.error_message3 = "\n *** Chromedriver Error Found Please Read REDME FILE For Configuration *** \n"
        self.error_message4 = "\n *** Some Errors Found Please Give It Back To Maintenance *** \n"
        self.error_message5 = "\n *** Please Close Opened XLSX Sheet An Try It Again OR Restart Application *** \n"
        self.error_message6 = "\n *** Taking Longer Time To Load URL Please Restart Application *** \n"
        self.input_text = ""
        self.browser = driver_setup()
        self.headers = ["Date","Title","Categories", "Lyrics","Tag"]
        self.category = ""

    def remove_multi_space(self, string):
        text = re.sub('\s+', ' ', string)
        return text.strip()

    def remove_html_text(self, string):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', string)
        return cleantext

    def sent_error_message(self, message):
        print(message)
        wx.MessageBox(message.replace("\n",""), 'Error', wx.OK | wx.ICON_ERROR)

    def startup(self):
        for count, link in enumerate(self.list_of_language):
            self.type = link.split("/")[-2].strip().capitalize().replace("-"," ")
            self.input_text += f'{count} => {self.type}\n'
        error = 0
        while True:
            number = input(f'{self.input_text}\nSelect Lyrics Category (NUMBER): ')
            if(self.regex.search(number) == None):
                index = int(number.strip())
                if len(self.list_of_language) >= index:
                    print(f"Selected : {self.list_of_language[index]}")
                    self.category = self.list_of_language[index].split("/")[-2].strip().capitalize().replace("-"," ")
                    time.sleep(2)
                    if self.browser != False:
                        error = 0
                        while True:
                            try:
                                self.browser.get(self.list_of_language[index])
                                time.sleep(4)
                                return self.browser
                            except Exception as e:
                                if error == 4:
                                    error_log(e)
                                    self.sent_error_message(self.error_message6)
                                else:
                                    time.sleep(3)
                                    error += 1
                    else:
                        self.sent_error_message(self.error_message3)
                else:
                    self.sent_error_message(self.error_message1)
            else:
                self.sent_error_message(self.error_message2)
    
    def fetch_links(self, browser):
        lyrics_links = []
        error = 0
        next_page_found = True
        while next_page_found == True:
            try:
                for link in browser.find_elements_by_xpath('//div[@class="posts-wrapper"]/article/div/div/h2/a'):
                    lyrics_links.append(link.get_attribute('href'))
                    
                next_page_found = False

                for next_page in browser.find_elements_by_xpath('//a[@class="next page-numbers"]'):
                    browser.get(next_page.get_attribute("href"))
                    time.sleep(2)
                    next_page_found = True
                    break
            except Exception as e:
                if error == 4:
                    error_log(e)
                    self.sent_error_message(self.error_message4)
                    input('Please Enter To Exit')
                    quit()
                else:
                    time.sleep(3)
                    error += 1
                    next_page_found = True
        return lyrics_links, browser
                
    def scrap_data(self, browser, links):
        try:
            date = datetime.now().strftime("%Y-%m-%d-%H.%M")
            filename = f"./{date} {self.category} Data.xlsx"
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet(datetime.now().strftime("Time %H-%M-%S"))

            for col,header in enumerate(self.headers):
                worksheet.write(0,col, header)
        except Exception as e:
            error_log(e)
            self.sent_error_message(self.error_message5)

        row = 2
        done = 0
        load_error = 0
        error_links = []
        for link in links:
            print("="*132)
            print(f"Loading URL ... {link} ")
            title = ""
            publish_date = ""
            song_details = ""
            actual_lyrics = ""
            main_error = 0
            while True:
                try:
                    error = 0
                    while True:
                        try:
                            browser.get(link)
                            time.sleep(3)
                            break
                        except Exception as e:
                            if error == 4:
                                error_log(e)
                                # self.sent_error_message(self.error_message6)
                            else:
                                print(f"Retrying ... {link} ")
                                time.sleep(3)
                                error += 1
                    
                    for get_title in browser.find_elements_by_xpath('//h1[@class="title entry-title"]'):
                        title = get_title.get_attribute('innerText').replace(" | ",", ").replace("|",", ").replace(" & ",", ").replace("&",", ").strip()
                        break
                    # print("Title: ",title)
                    
                    for get_date in browser.find_elements_by_xpath('//time[@class="entry-date published"]'):
                        publish_date = get_date.get_attribute('innerText').strip()
                        break
                    # print("Date: ",publish_date)

                    
                    for contain_data in browser.find_elements_by_xpath('//div[@class="nv-content-wrap entry-content"]/p'):
                        data = contain_data.get_attribute("innerText").lower().strip()

                        if (data.__contains__('song –') == True and data.__contains__("singer –") == True) \
                            or (data.__contains__('song: ') == True and data.__contains__("singer: ") == True)\
                            or (data.__contains__('song –') == True and data.__contains__("singers –") == True)\
                            or (data.__contains__('song: ') == True and data.__contains__("singer: ") == True):
                            song_details = data.lower()
                            break
                        else:pass
                    # print("song_details: ",song_details)
                    lyrics_type = ""
                    lyrics_path = ["h2","h3"]
                    for path in lyrics_path:
                        for lyrics_type in browser.find_elements_by_xpath(f'//div[@class="nv-content-wrap entry-content"]/{path}'):
                            lyrics_type = lyrics_type.get_attribute("innerText").strip()
                            if lyrics_type !="":break
                            # print(lyrics_type)
                            
                        if lyrics_type !="":break

                    # print("lyrics_type: ",lyrics_type)
                    
                    for lyrics in browser.find_elements_by_xpath("//p[contains(@style,'text-align: center;')]"):
                        actual_lyrics += lyrics.get_attribute("innerText").replace("\n","<BR>").strip()
                    # print("Lyrics: ",actual_lyrics)

                    updated_song_details = song_details.replace('\n','<BR>')
                    data = re.findall(r"(?<=–).*?(?=<BR>)", updated_song_details)
                    # print("data: ",data)
                    if len(data) == 0:data = re.findall(r"(?<=:).*?(?=<BR>)", updated_song_details)
                    updated_actual_lyrics = f"{lyrics_type}<BR><BR><BR>{actual_lyrics}<BR><BR><BR><BR>{self.remove_multi_space(updated_song_details)}"
                    updated_tag = f"{lyrics_type}"
                    for song_tag in data:
                        updated_tag += f",{song_tag.strip()}"
                        # print("updated_tag: ",updated_tag)
                    worksheet.write(row, 0, publish_date)
                    worksheet.write(row, 1, title)
                    worksheet.write(row, 2, self.category)
                    worksheet.write(row, 3, updated_actual_lyrics)
                    worksheet.write(row, 4, updated_tag.replace(', ',','))

                    row += 1
                    done += 1
                    # print(f"\n{'='*80}\n{publish_date}\n{title}\n{self.category}\n{updated_actual_lyrics}\n{updated_tag}\n{'='*80}\n")
                    break
                except Exception as e:
                    if main_error == 4:
                        error_log(e)
                        load_error += 1
                        error_links.append(link)
                        break
                    else:
                        time.sleep(3)
                        print(f"Retrying ... {link} ")
                        main_error += 1
            print(f"*** Total URL: {str(len(links))} Done: {str(done)} Failed To Load: {str(load_error)} ***")
            print("*** WARNING : PLEASE DON'T CLOSE APPLICATION UNTIL ALL PROCESS DONE (Data wiil be save after all links mined successfully done) ***")
        workbook.close()
        browser.close()
        for count, i in enumerate(error_links):
            print(f"Failed To Load (LINKS No. {str(count)}): {i}")
        
lyricsthings = LyricsThings()
browser = lyricsthings.startup()
links, browser = lyricsthings.fetch_links(browser)
result = lyricsthings.scrap_data(browser,links)

wx.MessageBox("Data Mining Successfully Done", 'Success', wx.OK | wx.ICON_INFORMATION)
input('Please Enter To Exit')
quit()
def warn(*args, **kwargs):
    pass
import sys
import warnings
warnings.warn = warn
import time
from config import driver_setup , error_log
import re,os
import csv
from datetime import datetime
import wx
app = wx.App()

class LyricsThings:

    def __init__(self):

        self.list_of_language = [
            "https://lyrics.agurchand.com/category/english-lyrics/",
            "https://lyrics.agurchand.com/category/hindi-lyrics/",
            "https://lyrics.agurchand.com/category/hindi-lyrics/old-lyrics-hindi-lyrics/",
            "https://lyrics.agurchand.com/category/kannada-lyrics/",
            "https://lyrics.agurchand.com/category/malayalam-lyrics/",
            "https://lyrics.agurchand.com/category/tamil-lyrics/",
            "https://lyrics.agurchand.com/category/tamil-lyrics/old-tamil-lyrics/",
            "https://lyrics.agurchand.com/category/telugu-lyrics/",
            "https://lyrics.agurchand.com/category/telugu-lyrics/page/21/"
        ]
        self.regex = re.compile('[a-zA-Z@_!#$%^&*()<>?/\|}{~:]')
        self.error_message1 = "\n *** Please Enter Valid Number *** \n"
        self.error_message2 = "\n *** Please Enter Number Without Any Letters or Special Character  *** \n"
        self.error_message3 = "\n *** Chromedriver Error Found Please Read REDME FILE For Configuration *** \n"
        self.error_message4 = "\n *** Some Errors Found Please Give It Back To Maintenance *** \n"
        self.error_message5 = "\n *** Please Close Opened CSV Sheet An Try It Again OR Restart Application *** \n"
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
        
        date = datetime.now().strftime("%Y-%m-%d-%H.%M")
        filename = f"./{date} {self.category} Data.csv"
        with open(filename, mode='w',newline='',encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()

            done = 0
            load_error = 0
            next_page_found = True
            while next_page_found == True:
                print("="*100)
                print(f"Loading URL ... {browser.current_url} ")
                total_data = browser.find_elements_by_xpath('//*[@id="contentwrap"]/div[1]/div/div[1]/p[1]')
                for div_count in range(1, len(total_data)+1, 1):
                    try:
                        title = ""
                        publish_date = ""
                        song_details = ""
                        actual_lyrics = ""
                        category = ""
                        tags = ""
                        for pub_date in browser.find_elements_by_xpath(f'//*[@id="contentwrap"]/div[1]/div[{str(div_count)}]/div[1]/p[1]'):
                            publish_date = re.sub('\s+', ' ',pub_date.get_attribute('innerText').strip())
                            break
                        # print("publish_date: ",publish_date)
                    
                        for title_br in browser.find_elements_by_xpath(f'//*[@id="contentwrap"]/div[1]/div[{str(div_count)}]/div[2]/h2[1]/a[1]'):
                            title = re.sub('\s+', ' ',title_br.get_attribute('innerText').strip())
                            break
                        # print("title: ",title)

                        for get_category in browser.find_elements_by_xpath(f'//*[@id="contentwrap"]/div[1]/div[{str(div_count)}]/div[2]/div/p[1]/span[contains(text(),"Category:")]/a'):
                            category =  re.sub('\s+', ' ',get_category.get_attribute('innerText').strip()) 
                
                        if category == "":
                            category = self.category
                        
                        for get_tags in browser.find_elements_by_xpath(f'//*[@id="contentwrap"]/div[1]/div[{str(div_count)}]/div[2]/div/p[1]/span[contains(text(),"Tags:")]/a'):
                            tags += re.sub('\s+', ' ',get_tags.get_attribute('innerText').strip()) + ","
                            
                        for contain_data in browser.find_elements_by_xpath(f'//*[@id="contentwrap"]/div[1]/div[{str(div_count)}]/div[2]/p'):
                            data = re.sub('\s+', ' ', contain_data.get_attribute("outerHTML").lower().strip())
                            if ("<img" not in data):
                                if (data.__contains__('music')) or (data.__contains__("lyrics"))\
                                    or (data.__contains__('lyricist')) or (data.__contains__("film"))\
                                    or (data.__contains__('singer')) or (data.__contains__("music director")) or (data.__contains__("singer(s)"))\
                                    or (data.__contains__("song")) or (data.__contains__("movie")):
                                    if ":" in data:
                                        song_details_list = re.findall(r"(?<=<strong>).*?(?=<br>)", data)
                                        if len(song_details_list) == 0:
                                            song_details_list = data.split("<br>")
                                        for detail in song_details_list:
                                            song_details += self.remove_html_text(detail).replace("</strong>",'').replace(", ",',').replace("<p>",'').replace("<p>",'').replace(": ",':').replace(" :",': ').replace("&nbsp;",'')+"<BR>"
                                            tags += detail.replace("</strong>",'').replace(", ",'').replace("&nbsp;",'').partition(":")[2].strip()+","
                                    break
                        song_details = re.sub('\s+', ' ', song_details)
                        print("\nsong_details: ",song_details)
                        if title.__contains__('–') == True:
                            lyrics_type = title.partition("–")[0].strip()

                        # print("lyrics_type: ",lyrics_type)

                        for lyrics in browser.find_elements_by_xpath(f'//*[@id="contentwrap"]/div[1]/div[{str(div_count)}]/div[2]/p'):
                            lyrics_data = lyrics.get_attribute("innerText").lower().replace("\n","<BR>").strip()
                            if (lyrics_data.__contains__('lyrics:')) == True or (lyrics_data.__contains__("music:"))\
                                or (lyrics_data.__contains__('lyricist:')) or (lyrics_data.__contains__("film:"))\
                                or (lyrics_data.__contains__('singer:')) or (lyrics_data.__contains__("music director")) or (lyrics_data.__contains__("singer(s)"))\
                                or (lyrics_data.__contains__("song:")):
                                pass
                            else:
                                actual_lyrics += lyrics_data.strip()
                        # print("Lyrics: ",actual_lyrics)
                        
                        updated_actual_lyrics = f"{lyrics_type}<BR><BR><BR>{actual_lyrics}<BR><BR><BR><BR>{self.remove_multi_space(song_details.rstrip('<BR>'))}"
                        # print("updated_tag: ",updated_actual_lyrics)
                        updated_tag = lyrics_type +","+ tags.rstrip(",")
                        # print("updated_tag: ",updated_tag)

                        if "<BR><BR><BR><BR><BR><BR><BR>" not in updated_actual_lyrics:
                            detail_dic = {
                                self.headers[0] : publish_date,
                                self.headers[1] : title,
                                self.headers[2] : category,
                                self.headers[3] : updated_actual_lyrics.rstrip('<BR><BR><BR><BR>'),
                                self.headers[4] : updated_tag.replace(', ',',').rstrip(',')
                            }
                            writer.writerow(detail_dic)
                            done += 1
                            print(f"***  Total URL: {str(len(links))} Done: {str(done)} Failed To Load: {str(load_error)} ***")

                    except Exception as e:
                        error_log(e)
                        next_page_found = True
                
                if next_page_found == True:
                    try:
                        next_page_found = False
                        for next_page in browser.find_elements_by_xpath('//*[@class="alignleft"]/a'):
                            browser.get(next_page.get_attribute('href'))
                            time.sleep(4)
                            next_page_found = True
                    except Exception as e:
                        error_log(e)
                        next_page_found = True
        return 
lyricsthings = LyricsThings()
browser = lyricsthings.startup()
links, browser = lyricsthings.fetch_links(browser)
lyricsthings.scrap_data(browser,links)

wx.MessageBox("Data Mining Successfully Done", 'Success', wx.OK | wx.ICON_INFORMATION)
input('Please Enter To Exit')
import sys
sys.exit("Thank You ")
exit(0)
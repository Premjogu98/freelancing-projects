import time

from config import driver_setup , error_log
import re,os
import xlsxwriter
from datetime import datetime
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
        self.valid_message1 = "\n *** Please Enter Valid Number *** \n"
        self.valid_message2 = "\n *** Please Enter Number Without Any Letters or Special Character  *** \n"
        self.valid_message3 = "\n *** Chromedriver Error Found Please Read REDME FILE For Configuration *** \n"
        self.valid_message4 = "\n *** Some Errors Found Please Give It Back To Maintenance *** \n"
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

    def startup(self):
        for count, link in enumerate(self.list_of_language):
            self.category = link.split("/")[-2].strip().capitalize().replace("-"," ")
            self.input_text += f'{count} => {self.category}\n'

        while True:
            number = input(f'{self.input_text}\nSelect Lyrics Category (NUMBER): ')
            if(self.regex.search(number) == None):
                index = int(number.strip())
                if len(self.list_of_language) >= index:
                    print(f"Selected : {self.list_of_language[index]}")
                    time.sleep(2)
                    if self.browser != False:
                        self.browser.get(self.list_of_language[index])
                        time.sleep(4)
                        return self.browser
                    else:
                        print(self.valid_message3)
                else:
                    self.valid_message1
            else:
                self.valid_message2
    
    def fetch_links(self, browser):
        lyrics_links = []
        next_page_found = True
        while next_page_found == True:
            try:
                for link in browser.find_elements_by_xpath('//div[@class="posts-wrapper"]/article/div/div/h2/a'):
                    lyrics_links.append(link.get_attribute('href'))
                    
                next_page_found = False

                # for next_page in browser.find_elements_by_xpath('//a[@class="next page-numbers"]'):
                #     browser.get(next_page.get_attribute("href"))
                #     time.sleep(2)
                #     next_page_found = True
                #     break
            except Exception as e:
                error_log(e)
                print(self.valid_message4)
                next_page_found = False
                input('Please Enter To Exit')
                quit()
        return lyrics_links, browser
                
    def scrap_data(self, browser, links):
        
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"./{date} {self.category} Data.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet(datetime.now().strftime("Time %H-%M-%S"))

        for col,header in enumerate(self.headers):
            worksheet.write(0,col, header)
            
        for row, link in enumerate(links, start=2):
            try:
                print(f"Mining Data: {link}")
                browser.get(link)
                time.sleep(3)
                
                title = ""
                for get_title in browser.find_elements_by_xpath('//h1[@class="title entry-title"]'):
                    title = get_title.get_attribute('innerText').replace(" | ",", ").replace("|",", ").replace(" & ",", ").replace("&",", ").strip()
                    # print(title)
                    break

                publish_date = ""
                for get_date in browser.find_elements_by_xpath('//time[@class="entry-date published"]'):
                    publish_date = get_date.get_attribute('innerText').strip()
                    # print(publish_date,'\n')
                    break
                
                song_details = ""
                for contain_data in browser.find_elements_by_xpath('//div[@class="nv-content-wrap entry-content"]/p'):
                    data = contain_data.get_attribute("innerText").lower().strip()

                    if (data.__contains__('song –') == True and data.__contains__("singer –") == True) \
                        or (data.__contains__('song: ') == True and data.__contains__("singer: ") == True)\
                        or (data.__contains__('song –') == True and data.__contains__("singers –") == True)\
                        or (data.__contains__('song: ') == True and data.__contains__("singer: ") == True):
                        song_details = data.lower()
                        # print(song_details,'\n')
                        break
                    else:
                        print("NO DATA FOUND")
                
                lyrics_type = ""
                lyrics_path = ["h2","h3"]
                for path in lyrics_path:
                    for lyrics_type in browser.find_elements_by_xpath(f'//div[@class="nv-content-wrap entry-content"]/{path}'):
                        lyrics_type = lyrics_type.get_attribute("innerText").strip()
                        print(lyrics_type)
                        break
                    if lyrics_type !="":break

                actual_lyrics = ""
                for lyrics in browser.find_elements_by_xpath("//p[contains(@style,'text-align: center;')]"):
                    actual_lyrics += lyrics.get_attribute("innerText").replace("\n","<BR>").strip()

                updated_song_details = song_details.replace('\n','<BR>')
                data = re.findall(r"(?<=–).*?(?=<BR>)", updated_song_details)
                if len(data) == 0:data = re.findall(r"(?<=:).*?(?=<BR>)", updated_song_details)
                updated_actual_lyrics = f"{lyrics_type}<BR><BR><BR>{actual_lyrics}<BR><BR><BR><BR>{self.remove_multi_space(updated_song_details)}"
                updated_tag = f"{lyrics_type}"
                for song_tag in data:
                    updated_tag += f",{song_tag.strip()}"

                worksheet.write(row, 0, publish_date)
                worksheet.write(row, 1, title)
                worksheet.write(row, 2, self.category)
                worksheet.write(row, 3, updated_actual_lyrics)
                worksheet.write(row, 4, updated_tag)

                print(f"\n============================================\n{publish_date}\n{title}\n{self.category}\n{updated_actual_lyrics}\n{updated_tag}\n============================================\n")
            except Exception as e:
                error_log(e)
        workbook.close()
        
lyricsthings = LyricsThings()
browser = lyricsthings.startup()
links, browser = lyricsthings.fetch_links(browser)
result = lyricsthings.scrap_data(browser,links)

print(result)
import time

from config import driver_setup , error_log
import re,os
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

    def startup(self):

        for count, link in enumerate(self.list_of_language):
            self.input_text += f'{count} => {link.split("/")[-2].strip().capitalize()}\n'

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
    
    def main(self, browser):
        lyrics_links = []
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
                error_log(e)
                print(self.valid_message4)
                next_page_found = False
                input('Please Enter To Exit')
                quit()
        return lyrics_links
                

lyricsthings = LyricsThings()
browser = lyricsthings.startup()
result = lyricsthings.main(browser)

print(result)
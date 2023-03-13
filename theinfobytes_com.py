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
import requests
import wx
from csv_to_xlsx import csv_to_xlsx
from config import driver_setup , error_log
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
        if not self.browser:
            self.sent_error_message(self.error_message3)
        self.main_filter = []
        self.main_filter_dict = {}
        try:
            print("WAIT Login process running....")
            self.browser.get("https://theinfobytes.com/wp-admin/edit.php")
            for username in self.browser.find_elements_by_id("user_login"):
                username.send_keys("Prem")
                time.sleep(1)
                break
            for password in self.browser.find_elements_by_id("user_pass"):
                password.send_keys("prem@2023")
                time.sleep(1)
                break
            for login in self.browser.find_elements_by_id("wp-submit"):
                login.click()
                time.sleep(5)
                break
            for get_category in self.browser.find_elements_by_xpath('//*[@id="cat"]/option[contains(text(),"LYRICS")]'):
                tags = get_category.get_attribute("innerText").strip().lower()
                category_val = get_category.get_attribute("value").strip()
                self.main_filter_dict[tags] = category_val
                self.main_filter.append(tags)
            # print(self.main_filter,'\n',self.main_filter_dict)
            print("Login Successfullyyyyyy")
        except Exception as e:
            error_log(e)
            self.sent_error_message(self.error_message4)
            self.browser.quit()
            exit(0)
        
        self.headers = ["Date","Title","Categories", "Lyrics","Tag"]
        self.regex = re.compile('[a-zA-Z@_!#$%^&*()<>?/\|}{~:]')
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
            print("***  Please Enter YEAR (should be 2023) OR MONTH (should be year + month ie., 202301 or 202302)  ***")
            self.date_or_year = input(f'Enter Year or Month : ').strip()
            if (self.regex.search(self.date_or_year) == None):
                self.date_or_year = int(self.date_or_year)
                break
            else:
                print(self.error_message2)
        self.user_selected_option = self.main_filter[self.selected_main_filter]


    def songs_scrap(self):
        
        self.browser.get(f"https://theinfobytes.com/wp-admin/edit.php?post_status=all&post_type=post&m={self.date_or_year}&cat={self.main_filter_dict[self.user_selected_option]}&post_format&filter_action=Filter&paged=1")
        time.sleep(2)
        if len(self.browser.find_elements_by_xpath('//tr[@class="no-items"]')) != 0:
            message = f" NO DATA FOUND FOR THIS FILTERS : ( {self.user_selected_option} ) ({self.date_or_year})"
            self.sent_error_message(message)
            self.browser.quit()
            import sys
            sys.exit("Thank You ")
        total_data_text = None
        for total_data in self.browser.find_elements_by_class_name('displaying-num'):
            total_data_text = int(total_data.get_attribute("innerText").replace('items','').replace(',','').strip())
            break
        print(f"\nTotal Data Found ==>  {total_data_text}")
        total_pages_text = None
        for total_pages in self.browser.find_elements_by_class_name('total-pages'):
            total_pages_text = int(total_pages.get_attribute("innerText"))
            break
        print(f'\nTOTAL PAGES FOUND : {total_pages_text}')
        if total_pages_text != 1:
            page_range = input(f'Enter Page Range eg.,(0-2 or 5-10) ==> ')
            from_page = int(page_range.partition("-")[0].replace('-','').strip())
            to_page = int(page_range.partition("-")[2].replace('-','').strip())
        else:
            from_page = 1
            to_page = 1

        date = datetime.now().strftime("%Y-%m-%d-%H.%M")
        filename = f"./{date} {self.user_selected_option}_{self.date_or_year} Data.csv"
        pending_data = []
        with open(filename, mode='w',newline='',encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()

            total_link = 1
            for page in range(from_page , to_page+1,1):
                self.browser.get(f"https://theinfobytes.com/wp-admin/edit.php?post_status=all&post_type=post&m={self.date_or_year}&cat={self.main_filter_dict[self.user_selected_option]}&post_format&filter_action=Filter&paged={page}")
                time.sleep(2)
                # print(len(self.browser.find_elements_by_xpath('//*[@id="the-list"]/tr')))
                total_tr = len(self.browser.find_elements_by_xpath('//*[@id="the-list"]/tr')) 
                for tr_count  in range(1, total_tr + 1,1):
                    title_text = ''
                    category_text = ''
                    tags_text = ''
                    released_date_text = ''
                    lyric_nav_link_text = ''
                    try:
                        for title in self.browser.find_elements_by_xpath(f'//*[@id="the-list"]/tr[{tr_count}]/td[1]/strong'):
                            title_text = title.get_attribute("innerText")
                            break
                        # print(title_text)

                        for category in self.browser.find_elements_by_xpath(f'//*[@id="the-list"]/tr[{tr_count}]/td[3]/a'):
                            category_text += f'{category.get_attribute("innerText")},'
                        category_text = category_text.strip().rstrip(',')
                        # print(category_text)

                        for tags in self.browser.find_elements_by_xpath(f'//*[@id="the-list"]/tr[{tr_count}]/td[4]/a'):
                            tags_text += f'{tags.get_attribute("innerText")},'
                        tags_text = tags_text.strip().rstrip(',')
                        # print(tags_text)

                        for released_date in self.browser.find_elements_by_xpath(f'//*[@id="the-list"]/tr[{tr_count}]/td[6]'):
                            released_date_text = released_date.get_attribute("innerText").replace('Published','').strip()
                            break
                        # print(released_date_text)

                        for lyric_nav_link in self.browser.find_elements_by_xpath(f'//*[@id="the-list"]/tr[{tr_count}]/td[1]/div[3]/span[4]/a'):
                            lyric_nav_link_text = lyric_nav_link.get_attribute("href")
                            break
                        # print(lyric_nav_link_text)
                        
                        resp = requests.get(lyric_nav_link_text,timeout=30)
                        if resp.status_code == 200:
                            html_data = re.sub(' +', ' ', resp.text)
                            lyrics_data = html_data.partition('class="entry-content">')[2].partition("</div>")[0].strip()
                        else:
                            raise Exception

                        detail_dic = {
                            self.headers[0] : released_date_text,
                            self.headers[1] : title_text,
                            self.headers[2] : category_text,
                            self.headers[3] : lyrics_data,
                            self.headers[4] : tags_text
                        }
                        writer.writerow(detail_dic)
                        print(f'PAGE {str(from_page)}/{str(to_page)} == Link {str(total_link)}/{str(total_data_text)} --> {lyric_nav_link_text}')
                        total_link += 1
                    except Exception as e:
                        error_log(e=e,source_page="theinfobytes.com")
                        pending_data.append({'title':title_text,'category':category_text,'tags':tags_text,'released date':released_date_text,'lyrics_link':lyric_nav_link_text})
        
        print("\n\nFILE EXPORTING...........")
        if csv_to_xlsx(filename,filename.replace(".csv",".xlsx")):
            print(f"\nFILE EXPORTED: {filename.replace('.csv','.xlsx')}\n")
        else:
            print("\n\nFILE EXPORITNG FAILED !!!")
            wx.MessageBox("FILE EXPORITNG FAILED !!! >>> EXPECTED EXE MAINTEINANCE <<< ", 'ERROR', wx.OK | wx.ICON_ERROR)

        os.remove(filename)
        self.browser.close()
        import json
        for data in pending_data:
            print(json.dumps(data, indent=2))
lyricsthings = LyricsThings()
lyricsthings.user_input()
lyricsthings.songs_scrap()


wx.MessageBox(">>>>>  Data Mining Successfully Done <<<<< \n(PLEASE CHECK COMMAND PROMPT IF ANY MISSING DETAILS ARE THERE DO MANUAL ENTERY )", 'Success', wx.OK | wx.ICON_INFORMATION)
# input('Please Enter To Exit')
# import sys
# sys.exit("Thank You ")
# exit()
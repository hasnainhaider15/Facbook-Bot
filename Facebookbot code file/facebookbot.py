from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
import os.path
import random
from datetime import datetime
import sys

class FacebookAutomation:

    def get_browser(self):
        try:
            loc = "chromedriver.exe"
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("user-data-dir=facebook")
            # options.add_argument("--log-level=OFF")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 1 })
            return webdriver.Chrome(executable_path=loc, chrome_options=options), "Success"
        except Exception as e:
            return None, e

    def login(self):

        with open("credentials.txt" , 'r') as f:
            lines = f.readlines()
            USERNAME = lines[0].strip()
            PASSWORD = lines[1].strip()
        
        self.browser.get("https://www.facebook.com")
        is_login = False

        try:
            email_input = self.browser.find_element_by_id('email')
            email_input.send_keys(USERNAME)
            email_input.send_keys(Keys.TAB)
            actions = ActionChains(self.browser)
            actions.send_keys(PASSWORD)
            actions.perform()
            actions = ActionChains(self.browser)
            actions.send_keys(Keys.RETURN)
            actions.perform()
            sleep(2)
            try:
                element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[text()="Log In"]' ))
                )

                is_login = False
            except:
                is_login = True
            
        
        except:
            ## no need to login because there is no login button on url "facebook.com" so there is no login form
            is_login = True

        return is_login

            
    def __init__(self):
        input("Press Enter to continue: ")
        self.browser, message = self.get_browser()
        if self.browser is None:
            print(message)
            input()
            exit()

        is_successful = self.login()
        
        if not is_successful:
            print("Check credentials")
            
        else:
            while True: 
                print("-------------Automation Menu---------------")
                print("1. Send message to Group members")
                print("2. Send message to Individual person") 
                try:
                    firstMenuInput = int(input("Enter your choice: "))   
                    if firstMenuInput == 1:
                        self.message_to_group_members()
                    elif firstMenuInput == 2:
                        self.message_to_individual_person()   
                    else:
                        print("Wrong input!!!")
                        continue
                    break
                except ValueError:
                    print("Use integer number in input ")
                    continue

    def details(self):
        
        if self.callFromFunction == True:
            self.search_query = input("Enter group name: ")
            while True:
                try:
                    self.group_limit = int(input("Enter no of groups to procced: "))
                    self.people_limit = int(input("Enter people limit: "))
                    
                except:
                    print("Enter integer number")
                    continue
                break  
            self.location_input = input("Enter location to sort groups: ") 
            self.people_limit = self.people_limit * 2
        elif self.callFromFunction == False:
            self.search_query = input("Enter person name: ")
            while True:
                try:
                    self.people_limit = int(input("Enter people limit: "))
                except:
                    print("Enter integer number")
                    continue
                break   
        
    def message_to_group_members(self): 
        self.callFromFunction= True
        self.details()
        sleep(1)

        group_query_url = "https://www.facebook.com/groups/search/groups/?q=" + self.search_query
        self.browser.get(group_query_url)
        sleep(2)
        divs_inside = self.browser.find_elements_by_xpath("//div[@class='ipjc6fyt dflh9lhu r8blr3vg']/div")
        my_group = divs_inside[-1]
        my_group = my_group.find_element_by_tag_name("input").click()
        sleep(1)
        
        location = divs_inside[0].click()
        actions = ActionChains(self.browser)
        actions.send_keys(self.location_input)
        actions.perform()
        sleep(1)

        actions = ActionChains(self.browser)
        actions.send_keys(Keys.DOWN)
        actions.perform()
        sleep(1)

        actions = ActionChains(self.browser)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        
        self.group_main_window = self.browser.current_window_handle
        
        sleep(2)
    
        members_link = []
       
        groups = self.browser.find_elements_by_xpath('//a[@class = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8"]')

        sleep(2)
        for group in groups:
            link = group.get_attribute("href")
            members = link + "members"
            members_link.append(members)

        members_link = members_link[:self.group_limit]

        for self.group_members in members_link:
            self.browser.execute_script("window.open();")
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.get(self.group_members)
            
            
            sleep(3)
            group_member_classes = self.browser.find_elements_by_xpath('//div[@class = "muag1w35 b20td4e0"]')
            group_member_section = group_member_classes[-1]
    
            tag = group_member_section.find_elements_by_tag_name("a")
            tag = tag[:self.people_limit:2]
            self.user_profile_id = [] 
            
            for v in tag:
                self.main_window = self.browser.current_window_handle
                self.window_index = False
                sleep(2)
                link = v.get_attribute("href")
                splited = link.split(sep = "/")
                id  = splited[-2]
                self.user_profile_id.append(id)
                self.send_friend_request(id)
             
            self.browser.close()
            # back to the main window
            self.browser.switch_to.window(self.group_main_window)
          
                     

    def getting_messenger_browser(self, id):
        
        message_url = 'https://www.facebook.com/messages/t/' + id
        self.browser.get(message_url)
        sleep(2)

        self.browser.switch_to.frame(self.browser.find_element_by_xpath('//iframe[@class = "k4urcfbm jgljxmt5 a8c37x1j izx4hr6d humdl8nn bn081pho gcieejh5"]'))
        sleep(2)

        name_text  = self.browser.find_element_by_xpath('//span[@class = "_3oh-"]')
        name = name_text.text
        message_data = self.load_message_from_file(name)

        sleep(1)
        messenger_textbox = self.browser.find_element_by_xpath('//div[@aria-label = "Type a message..."]')
        messenger_textbox.send_keys(message_data)
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        sleep(2)
        self.browser.switch_to.default_content()

    def send_friend_request(self, id):
        profile_url = 'https://www.facebook.com/' + id
        self.browser.execute_script("window.open();")
        if self.window_index == True:
            self.browser.switch_to.window(self.browser.window_handles[1])
        elif self.window_index == False:
            self.browser.switch_to.window(self.browser.window_handles[2])
        self.browser.get(profile_url)
        sleep(2)
        try:
            button = self.browser.find_element_by_xpath('//div[@aria-label = "Add Friend"]')
            button.click()
               
        except:
            pass
        
        self.getting_messenger_browser(id)
        self.browser.close()

        # back to the main window
        self.browser.switch_to.window(self.main_window)
        
        
        

    def load_message_from_file(self, namedata):
        with open('messages.txt', 'r') as f:
            messages = f.readlines()
            message =  random.choice(messages)
            message_data = message.replace("#NAME#", namedata)
            return message_data 


    def message_to_individual_person(self):
        self.callFromFunction = False
        self.details()

        indiviual_search = "https://www.facebook.com/search/people/?q=" + self.search_query
        self.browser.get(indiviual_search)
        sleep(2)

        persons = self.browser.find_elements_by_xpath('//a[@class = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p dkezsu63"]')

        sleep(3)
        people_links = []
        for person in persons: 

            link = person.get_attribute("href")
            people_links.append(link)
            
        
        people_links = people_links[:self.people_limit]
        for v in people_links:
            self.main_window = self.browser.current_window_handle
            self.window_index = True
            sleep(2)
            splited = v.split(sep = "/")
            id  = splited[-1]
            self.send_friend_request(id)



if __name__ == "__main__":
    try:
        deliver_date = datetime(2020, 9, 25, 0, 00)
        current_date = datetime.now()
        duration = current_date - deliver_date
        if duration.days < 3:
            instance = FacebookAutomation()

        input("Press Enter to Exit!!")
    except Exception as e:
        print(e)
        input()
   


 

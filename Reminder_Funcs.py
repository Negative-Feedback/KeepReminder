from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from twilio.rest import Client

def login_and_get_tasks(email, password):
    browser = webdriver.Chrome()  # using chrome as the browser
    browser.get('http://keep.google.com')  # go to keep notes
    browser.implicitly_wait(5)  # yeah idk, this line was prolly in the tutorial

    # the email textbox element
    emailElem = browser.find_element_by_id('identifierId')
    # type the email into the textbox
    emailElem.send_keys(email)

    # the next button element
    nextButton = browser.find_element_by_id('identifierNext')
    # click the button
    nextButton.click()

    # wait for the elements to load
    browser.implicitly_wait(2)

    # find the password text field
    passwordElem = browser.find_element_by_xpath("//input[@name='password']")
    # type the password and press enter
    passwordElem.send_keys(password + Keys.ENTER)

    # when you go to keep.google.com it automatically sends you go the login page
    # after you complete the login it redirects you to keep.google.com
    # so this loop is used to wait for the redirect
    while (browser.current_url != "https://keep.google.com/"):
        time.sleep(2.5)

    # get the page source and close the browser
    pageSource = browser.page_source
    browser.close()

    # using BeautifulSoup to scrape the source for the info I want
    pageSource = BeautifulSoup(pageSource, 'html.parser')

    # finding my note by the class id
    # to get the id of the note, i had to use the element inspector tool
    note = pageSource.find_all('div', class_="IZ65Hb-n0tgWb IZ65Hb-WsjYwc-nUpftc NYTeh-IT5dJd rymPhb RNfche")[1]
    # did the same thing here to get this class id
    entryList = note.find('div', class_="gkA7Yd-sKfxWe rymPhb-IZ65Hb-gkA7Yd")

    task_list = ""
    for entry in entryList.find_all('div', class_="CmABtb RNfche"):
        task_list = task_list + entry.text.strip() + '\n'

    return task_list

def send_message(phone_num, twilio_num, account_sid, auth_token, task_list):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_= twilio_num,
        body= task_list,
        to=phone_num)

def remind(email, password, phone_num, twilio_num, account_sid, auth_token):
    task_list = login_and_get_tasks(email, password)
    send_message(phone_num, twilio_num, account_sid, auth_token, task_list)
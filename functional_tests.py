from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert browser.title == 'The install worked successfully! Congratulations!'


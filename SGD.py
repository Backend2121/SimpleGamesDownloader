import os

# Check if pip exists if not install
if (os.system("pip -V") != 0):
    os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    os.system("python get-pip.py")
    os.remove("get-pip.py")

# Check if Selenium is already installed if not install 
try:
    from selenium import webdriver
except ModuleNotFoundError:
    os.system("pip install selenium")
from selenium.webdriver.chrome.options import Options

proxy = "https://hide.me/it/proxy"
# Results of the nxbrew search
links = []
# Contains hrefs poisoned by hide.me
poisonedLinks = []
# Chrome headless and silent options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')

class driver():
    # General class of the browser
    def __init__(self):
        self.Driver = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)

def Proxy(input, URL):
    # Navigate hide.me
    input.click()
    input.clear()
    input.send_keys(URL)
    input.submit()

def prettifyOutput(link):
    # Give advice on how to use the obtained information
    if ("magnet:?" in link):
        print("\nThis looks like a Torrent Magnet URL, open it up with Torrent!:\n" + link)
    else:
        print("\nThis looks like a normal URl, open it up on the browser!:\n" + link)

def CleanLink(userInput):
    # User error checking
    while (int(userInput) > len(poisonedLinks) - 1) or int(userInput) < 0:
        print("Invalid number\n")
        userInput = input("Which link you want do open? [0 - " + str(len(poisonedLinks)-1) + "]")
    
    # Link skippin'
    browser.get(poisonedLinks[int(userInput)])
    downloadLink = browser.find_element_by_xpath("/html/body/header/div/div/div/div[1]/a").get_attribute("href")
    browser.get(downloadLink)
    unpoisonedLink = browser.find_element_by_xpath('/html/body/div[1]/form/div/input').get_attribute("value")
    browser.get(unpoisonedLink)

def listGames(list):
    # Print out all results found during search
    for k,v in enumerate(list):
        print(str(k) + ": " + v.text + "\n")

def main():
    # Tunnel with Proxy
    browser.get(proxy)
    inputBox = browser.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div[2]/div/form/fieldset/div[1]/input')
    toSearch = input("Type here the game you want to search for: ")
    url = "https://nxbrew.com/search/"+toSearch+"/"
    Proxy(inputBox, url)

    # Index all results of the search specified in url -> toSearch
    # Ask the user the number corresponding to the desired game
    posts = browser.find_elements_by_class_name("post-title")
    for post in posts:
        links.append(post.find_element_by_xpath(".//*").get_attribute("href"))
    
    # Check for no results
    if len(links) == 0:
        print("\nNo results found!")
        browser.close()
        return

    # Clean user input for game selection
    listGames(posts)
    choice = input("Choose which one you want to download [0 - "+str(len(links)-1)+"]: ")
    while (int(choice) > len(links) - 1) or int(choice) < 0:
        print("Invalid number\n")
        choice = input("Which link you want do open? [0 - " + str(len(links)-1) + "]")
    browser.get(links[int(choice)])
    
    # Get download links
    # Ask the user the number corresponding to the desired download link
    downloadLinks = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/div/div/article/div[4]/div[3]/div[2]")
    downloadList = downloadLinks.find_elements_by_css_selector("p")
    for k,v in enumerate(downloadList):
        if (v.find_element_by_css_selector("a").get_attribute("href") != None and "[Decrypt Here]" not in v.text):
            # Get internal link poisoned by Hide.me
            print(str(k) + ": " + v.text + " \nInternal Link: " + v.find_element_by_css_selector("a").get_attribute("href") + "\n")
            poisonedLinks.append(v.find_element_by_css_selector("a").get_attribute("href"))
        else:
            # Used only in Base64 Encoded links TODO Date: TBD
            print("ERROR: BASE 64 DECODING NOT YET IMPLEMENTED \n" + v.text)
    if (len(poisonedLinks) == 1):
        choice = 0
    else:
        choice = input("Which link you want do open? [0 - " + str(len(poisonedLinks)-1) + "]")

    # Skippin' link shortners
    CleanLink(choice)

    # Bypass fake robot check by insta-killing javascript with 4 ESCAPE inputs
    for x in range(0, 4):
        browser.execute_script("window.stop();")

    # Wait for 3 seconds to end with while loop
    finalLink = browser.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
    while "javascript" in finalLink:
        finalLink = browser.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")

    # Print results out
    prettifyOutput(finalLink)

    # Kill the browser
    browser.close()

if __name__ == '__main__':
    # Start
    browser = driver().Driver
    main()
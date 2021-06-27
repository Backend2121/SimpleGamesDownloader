import os
from bs4 import BeautifulSoup

# Check if pip exists if not install
if (os.system("pip -V") != 0):
    os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    os.system("python get-pip.py")
    os.remove("get-pip.py")

# Check if Selenium is already installed if not install 
try:
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ModuleNotFoundError:
    print("WARNING: Selenium not installed, installing...")
    os.system("pip install selenium")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

# Check if BeautifulSoup4 is already installed if not install
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("WARNING: BeautifulSoup4 not installed, installing...")
    os.system("pip install beautifulsoup4")
    from bs4 import BeautifulSoup

proxy = "https://hide.me/it/proxy"
# Results of the nxbrew search
links = []
# Contains hrefs poisoned by hide.me
downloadLinks = []
# Chrome headless and silent options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')

class driver():
    # General class of the browser
    def __init__(self):
        try:
            self.Driver = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
        except:
            print("ERROR: Webdriver not found, please make sure you have it inside this script's folder!")

def Proxy(input, URL):
    # Navigate hide.me
    input.click()
    input.clear()
    input.send_keys(URL)
    input.submit()

def prettifyOutput(link):
    # Give advice on how to use the obtained information
    if ("magnet:?" in link):
        print("\nThis looks like a Torrent Magnet URL, open it up with a Torrent client!:\n" + link)
    else:
        print("\nThis looks like a normal URl, open it up on the browser!:\n" + link)

def CleanLink(userInput):
    # User error checking
    while (int(userInput) > len(downloadLinks) - 1) or int(userInput) < 0:
        print("Invalid number\n")
        userInput = input("Which link you want do open? [0 - " + str(len(downloadLinks)-1) + "]")
    
    # Link skippin'
    browser.get("https://nl.hideproxy.me" + downloadLinks[int(userInput)])
    downloadLink = browser.find_element_by_xpath("/html/body/header/div/div/div/div[1]/a").get_attribute("href")
    browser.get(downloadLink)
    unpoisonedLink = browser.find_element_by_xpath('/html/body/div[1]/form/div/input').get_attribute("value")
    browser.get(unpoisonedLink)

def listGames(list):
    # Print out all results found during search
    for k,v in enumerate(list):
        print(str(k) + ": " + v.text + "\n")

def scrape(htmlPage):
    #Step by step garbage cleaning of html page with BS4
    soup = BeautifulSoup(htmlPage, 'html.parser')
    n = 0
    for bigDiv in soup.find_all("div", class_="wp-block-columns has-2-columns"):
        for div in bigDiv.find_all("div", class_="wp-block-column"):
            for p in div.find_all("p"):
                #Get download name
                try:
                    print(p.find("strong").get_text(), end=":\n")
                except:
                    pass
                for a in p.find_all("a"):
                    print(a.get_text() + " " + a.get("href") + " [" + str(n) + "]")
                    downloadLinks.append(a.get("href"))
                    n = n + 1
    return downloadLinks
    
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
    # Currently lists only the first result found
    downloadLinks = scrape(browser.page_source)
    #downloadLinks = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/div/div/article/div[4]")
    #downloadLinks = downloadLinks.find_elements_by_class_name("wp-block-columns has-2-columns")

    #for k,v in enumerate(downloadLinks):
    #    link = v.find_element_by_css_selector("a").get_attribute("href")
    #    if (link != None and "[Decrypt Here]" not in v.text):
    #        # Get internal link poisoned by Hide.me
    #        print(str(k) + ": " + v.text + " \nInternal Link: " + link + "\n")
    #        poisonedLinks.append(link)
    #    else:
            # Used only in Base64 Encoded links TODO Date: TBD
    #        print("ERROR: BASE 64 DECODING NOT YET IMPLEMENTED \n" + v.text)
    # If only 1 result is found, proceed automatically
    if (len(downloadLinks) == 1):
        choice = 0
    else:
        choice = input("Which link you want do open? [0 - " + str(len(downloadLinks)-1) + "]")

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
    exit()
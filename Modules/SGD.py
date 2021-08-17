import os
from sys import implementation
from Modules.Prettifier import *

# Check if Pillow is already installed if not install 
try:
    from PIL import Image
except ModuleNotFoundError:
    print("WARNING: Pillow not installed, installing...")
    os.system("pip install Pillow")
    from PIL import Image

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
# Chrome headless and silent options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')

class SGD():
    """Switch Games Downloader main class"""
    def __init__(self):
        """Instantiate the Selenium browser, used throughout the entire process"""
        try:
            self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
        except:
            Error("Webdriver not found, please make sure you have it inside this script's folder!") 
    
    def Proxy(self, input, URL):
        # Navigate hide.me
        input.click()
        input.clear()
        input.send_keys(URL)
        input.submit()

    def CleanLink(self, userInput):
        """Final step: Unpoison download link"""
        # User error checking
        if "/go.php" not in userInput:
            return

        # Link skippin'
        userInput = userInput[userInput.find("/go.php"):]
        self.browser.get("https://nl.hideproxy.me" + userInput)
        downloadLink = self.browser.find_element_by_xpath("/html/body/header/div/div/div/div[1]/a").get_attribute("href")
        self.browser.get(downloadLink)
        unpoisonedLink = self.browser.find_element_by_xpath('/html/body/div[1]/form/div/input').get_attribute("value")

        # TEMPORARY FIX TO AVOID CAPTCHA BYPASSING, NEEDS USER INPUT
        return unpoisonedLink
        # TEMPORARY FIX TO AVOID CAPTCHA BYPASSING, NEEDS USER INPUT
        
        self.browser.get(unpoisonedLink)
        
        # Bypass fake robot check by insta-killing javascript with 4 ESCAPE inputs
        for x in range(0, 4):
            self.browser.execute_script("window.stop();")

        # Wait for 3 seconds to end with while loop
        finalLink = self.browser.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
        while "javascript" in finalLink:
            finalLink = self.browser.find_element_by_xpath("/html/body/div[1]/div/div/section/div/div/div/div/div[3]/a").get_attribute("href")
        
        return finalLink

    def scrape(self, htmlPage):
        """Find all link available for a certain title"""
        # Contains hrefs poisoned by hide.me
        self.downloadLinks = []
        self.downloadLabels = []
        #Step by step garbage cleaning of html page with BS4
        soup = BeautifulSoup(htmlPage, 'html.parser')
        for bigDiv in soup.find_all("div", class_="wp-block-columns has-2-columns"):
            for div in bigDiv.find_all("div", class_="wp-block-column"):
                for p in div.find_all("p"):
                    # Get download name
                    try:
                        self.downloadLinks.append(p.find("strong").get_text())
                        self.downloadLabels.append("- ")
                    except:
                        pass
                    # Get download name + link
                    for a in p.find_all("a"):
                        self.downloadLinks.append(a.get("href"))
                        self.downloadLabels.append(a.get_text())
        return (self.downloadLinks, self.downloadLabels)

    def searchGame(self, toSearch):
        """First step: Search through nxbrew"""
        # Reset Chromedriver
        try:
            self.browser.close()
            self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
        except:
            self.browser = webdriver.Chrome(executable_path=os.getcwd() + "//chromedriver.exe", chrome_options=chrome_options)
        
        # Clear cookies
        self.browser.delete_all_cookies()
        # Tunnel with Proxy
        self.browser.get(proxy)
        inputBox = self.browser.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div[2]/div/form/fieldset/div[1]/input')
        # toSearch = GUI InputBox
        # toSearch = input("Type here the game you want to search for: ")
        url = "https://nxbrew.com/search/"+toSearch+"/"
        # Proxy tunnel the request
        self.Proxy(inputBox, url)

    def listIcons(self):
        iconsLinks = []
        sizes = []
        icons = self.browser.find_elements_by_class_name("post-thumbnail")
        for icon in icons:
            # This are the links that need to be passed to the GUI for icon replacement
            height = int(icon.find_element_by_xpath(".//*/img").get_attribute("naturalHeight"))
            width = int(icon.find_element_by_xpath(".//*/img").get_attribute("naturalWidth"))
            sizes.append((height, width))
            iconsLinks.append(icon.find_element_by_xpath(".//*/img").get_attribute("src"))

        return iconsLinks, sizes

    def listGames(self):
        """Send all results found, after the search, to the GUI"""
        links = []
        # Index all results of the search specified in url -> toSearch
        posts = self.browser.find_elements_by_class_name("post-title")
        if not posts:
            if (self.browser.current_url == "https://nl.hideproxy.me/index.php"):
                return 1

        for post in posts:
            # This are the links that need to be passed to the browser for scrape()
            links.append(post.find_element_by_xpath(".//*").get_attribute("href"))

        # Check for no results
        if len(links) == 0:
            return 0
        
        # Return all results found during search to the GUI
        # infos [0] = v.text
        # infos [1] = links
        infos = [],[]
        for k,v in enumerate(posts):
            infos[0].append(v.text)
        infos[1].append(links)

        return infos

    def listLinks(self, link):
        """Get download links"""
        self.browser.get(link)
        # Ask the user the number corresponding to the desired download link
        downloadLinks = self.scrape(self.browser.page_source)
        return downloadLinks

    def cropImage(self, image, size):
        # Selenium screenshots the screen at a default resolution of 800x600
        # Size is a tuple containing height and width
        # ((800 - width)/2, (600 - height)/2) = top-left corner of icon
        # top-left + width & height = Icon
        """Grabs the game icon, removes the black borders"""
        boxArt = ((800-size[1])/2,(600-size[0])/2, (800-size[1])/2 + size[1], (600-size[0])/2 + size[0])
        img = Image.open(image, mode="r")
        cropped = img.crop(boxArt)
        os.remove(image)
        try:
            cropped.save(image)
        except SystemError as e:
            print("Error: " + e)
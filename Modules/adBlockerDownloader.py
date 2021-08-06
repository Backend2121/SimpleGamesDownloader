import requests
import os

def downloadAdBlocker():
    r = requests.get('https://clients2.google.com/service/update2/crx?response=redirect&prodversion=92.0.4515.131&acceptformat=crx2,crx3&x=id%3Dcfhdojbkjhnklbpkdaibdccddilifddb%26uc')

    with open(os.getcwd() + "\\Modules\\adblock.crx", "wb") as f:
        f.write(r.content)
        f.close()
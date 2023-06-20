# IT'S MULTITHREADING

from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json
from selenium.common.exceptions import *

optionla = Options();
optionla.add_argument("disable-notifications"); # 先把通知都關掉，不然後面會點不到按鈕
optionla.add_argument('--headless') # don't render the webpage per se, but more difficult to debug
optionla.add_argument('--disable-gpu') # prevent weird bug
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=optionla)

# file saving
from pathlib import Path
basedir = Path("directory_of_interest")

# Always check for base directory
if not basedir.is_dir():
    basedir.mkdir()


# the crawler per se

#自動化流程，跑這個就對了
def run_it(face):

    emoji, filename = face[0], face[1]
    #print(emoji, filename)
    # check if file exists or not
    if Path(basedir/(filename+".json")).is_file():
        print(f"{emoji} {filename} has been fetched, skip")
        return

    # make driver local to the function to run faster, little trick in python
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=optionla)

    TAR_URL = f"https://www.plurk.com/search?q={emoji}&date=2022-09"
    driver.get(TAR_URL)

    # "row to the bottom first"
    # "SUCCEEDED", while not at the buttom, scroll it!
    while len(driver.find_elements(By.XPATH, '//*[@id="result"]//*[@class="status-holder"]//*[@class="button"]')) == 0:
        driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + "document.body.scrollHeight,document.documentElement.clientHeight));")
        sleep(0.3)

    # "then get the data"
    # t = 0 # move this into the loop
    final = []
    #for t, ele in ...:
    posts = driver.find_elements('xpath', '//*[@class="content"]')
    final = [ele.text for ele in posts]

    with open(f"{basedir/filename}.json",'w', encoding = 'utf-8') as yyyyy:
        json.dump(final,yyyyy)
        yyyyy.close()

    print(f"{emoji} {filename} fetch succeeded")
    # close the driver / browser after the task for this emoji is done
    driver.quit()


if __name__ == "__main__":
    import multiprocessing
    import sys
    
    "e.g.,"
    tar_tmp = [
        "🤗 huggingface",
        "😁 grinningfacewithsmilingeyes", #Grinning face with smiling eyes')",
        "😆 grinningsquintingface"
    ]

    "split the target into [emoji, text] format"
    tar = [ele.split(" ") for ele in tar_tmp]
    "to record the processes"
    processes = []

    # does things (aka, search & fetch) in parallel
    for face in tar:
        p = multiprocessing.Process(target=run_it, args=(face,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()



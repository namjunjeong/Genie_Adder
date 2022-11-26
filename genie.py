def song_added(driver,gen):
    artist=driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[1]/span[2]').text
    genie_song_name=driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/h2').text
    print(artist+'-'+genie_song_name+' added in '+gen+'\n')
    driver.refresh()

    
#main code

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import sleep

###############chrome driver option and setting##################
#first of all, start chrome with debugging mode from cmd
#use experimental_option to use debug chrome
chrome_options=Options()
chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
chrome_driver="C:\Program Files (x86)\jj\chrome\chromedriver.exe"
driver=webdriver.Chrome(chrome_driver,options=chrome_options)
############################################################################
############################################################################
############################################################################
############################################################################
############################################################################
############################################################################
############################################################################


wait=WebDriverWait(driver,10)
genre=[]
song_file=open("my_song_file.txt",'r',encoding="utf-8")
etc=open("etc.txt",'wt',encoding="utf-8")
song_list=song_file.readlines()
for song in song_list:

    if(len(song)==0):
        print("list finish")
        break
    if(len(song)<=3):
        continue
    if('---' in song):
        continue
        
        
    #search song
    driver.find_element_by_xpath('//*[@id="sc-fd"]').clear()
    driver.find_element_by_xpath('//*[@id="sc-fd"]').send_keys(song)
    driver.find_element_by_xpath('//*[@id="frmGNB"]/fieldset/input[3]').click()

    #find info of song from search page
    try:
        driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr[1]/td[4]/a').click()
    except:
        print("can't find this song")
        etc.write(song+'\n')
        continue
    song_genre=driver.find_element_by_xpath('//*[@id="body-content"]/div[2]/div[2]/ul/li[3]/span[2]').text
    song_genre_list=song_genre.split('/')
    for i in range(len(song_genre_list)):
        song_genre_list[i]=song_genre_list[i].strip()
    for song_genre in song_genre_list:
        if(song_genre in genre):
            #add playlist already exist

            #xpath of playlist we have to use
            xpath_tmp='//*[@id="mCSB_1_container"]/li['+str(genre.index(song_genre)+1)+']/a'
            driver.find_element_by_xpath('//*[@id="add_my_album_top"]').click()
            try:
                driver.find_element_by_xpath(xpath_tmp).click()
            except:
                #change attribute related to scroll of playlist
                px=str((genre.index(song_genre)-4)*25*(-1))
                scroll_element=driver.find_element_by_xpath('//*[@id="mCSB_1_container"]')
                driver.execute_script("arguments[0].setAttribute('style','position: relative; top: {}px; left: 0px;')".format(px), scroll_element)
                driver.find_element_by_xpath(xpath_tmp).click()
            while True:
                try:
                    al=Alert(driver)
                    al.accept()
                    break
                except:
                    continue
            song_added(driver,song_genre)
        else:
            #create new playlist
            genre.insert(0,song_genre)
            print("new genre : "+song_genre+'\n')
            driver.find_element_by_xpath('//*[@id="add_my_album_top"]').click()
            driver.find_element_by_xpath('//*[@id="newMyAlbumName"]').send_keys(song_genre)
            driver.find_element_by_xpath('//*[@id="newMyAlbum"]').click()
            sleep(1)
            driver.find_element_by_xpath('//*[@id="my-album"]/div[2]/ul/li[1]/a').click()
            while True:
                try:
                    al=Alert(driver)
                    al.accept()
                    break
                except:
                    continue
            song_added(driver,song_genre)


song_file.close()
etc.close()
print("test finished")
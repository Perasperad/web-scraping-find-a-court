from datetime import date, time, datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options,
                          executable_path=r'C:\\Users\\tbart\\Desktop\\prenotazione\\chromedriver_win32\\chromedriver'
                                          r'.exe')
centri = ['justpadelaeronautica', 'empirepadel', 'palaluissondina', 'sportingostiensepadel', 'aureliapadel',
          'pinkpadelclub']
campi = [[6625, 6627, 25090, 6198, 4708], [34353, 37765, 37764, 11709, 11705, 11707, 20317, 20319, 20318], [35284, 35286, 35288],
         [26480, 26481, 26482, 35273, 26483, 35272, 35274, 28377, 28376], [4903, 4899, 4901, 37594, 10317, 37593], [7714, 7716, 38268]]
# justpadelaeronautica  8 coperto (60 min: 6624),4 scoperto (60 min: 6626), 2 scoperto (60 min: 25089), 5 scoperto (60 min:6197),
# 7 coperto (60 min: 4707) - COMPLETO
# palaluiss  1,2,3 - COMPLETO
# sportingostiense  - 1,2,3,4,5,8,7,6, campo centrale - COMPLETO
# empire - coperto, 3, 1, 2, coperto+, coperto*, coperto**, coperto++, coperto++** - COMPLETO
# aurelia - roland garros, us open, foro italico, wimbledon, world padel tour, grande slam - COMPLETO
# bailey =[20168, 20170, 20164, 20166, 20172] - A, B, C, D, E - COMPLETO
# justpadel =[3854, 3852, ] - bianco, rosso
# lamirage = [38578, 6310, 16550]  - A,B,C
# ymcaprime
# pinkpadelclub A, B, C - COMPLETO
# 6197, 6624, 38445, 25117

primo_lancio = 0  # il primo accesso necessita autenticazione

TELEGRAM_TOKEN = '1662982080:AAHEkUPaM9VICp0pism4pe7rWIoMJQfDiKM'
TELEGRAM_GROUP_CHAT_ID = '-1001469520839'
TELEGRAM_BOT_CHAT_ID = '661575172'

startTime = datetime.now()

payload = {
    'chat_id': TELEGRAM_GROUP_CHAT_ID,
    'text': "",
    'parse_mode': 'HTML',
    'disable_web_page_preview': 'TRUE'
}

for z in range(0, 6, 1):
    if primo_lancio == 0:
        # 1 | click | css=.modal-dialog > .close | pop up home
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-dialog > .close"))).click()
        driver.get("https://www.prenotauncampo.it/accedi-registrati/login/")
        try:
            click4 = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".panel-body .btn-fb")))
            driver.execute_script("arguments[0].click();", click4)  # to handle ElementClickInterceptedException
        except TimeoutException as e:
            print('pulsante FB non trovato')
        try:
            click5 = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Accetta tutti"]')))
            driver.execute_script("arguments[0].click();", click5)  # to handle ElementClickInterceptedException
        except TimeoutException as e:
            print('pulsante Cookies non trovato')

        driver.find_element(By.ID, "email").send_keys("t.bartolomei@yahoo.it")
        driver.find_element(By.ID, "pass").send_keys("Andreaavella88")

        try:
            click6 = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "loginbutton")))
            driver.execute_script("arguments[0].click();", click6)  # to handle ElementClickInterceptedException
        except TimeoutException as e:
            print('pulsante login non trovato')

        primo_lancio = 1

    driver.get("https://www.prenotauncampo.it/centri-sportivi/roma/roma/" + str(centri[z]))
    try:
        click7 = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-forward")))
        driver.execute_script("arguments[0].click();", click7)  # to handle ElementClickInterceptedException
    except TimeoutException as e:
        print('pulsante-freccia non trovato')

    for j in range(0, 4, 1):
        oggi = date.today()
        delta = timedelta(days=j)
        giorniAggiunti = oggi + delta


        def day(j):
            switcher = {
                0: 4,
                1: 5,
                2: 6,
                3: 7,
            }
            return switcher.get(j, "invalid day")

        continue_19 = "si"
        continue_19_30 = "si"
        continue_20 = "si"

        for i in range(0, len(campi[z]), 1):
            if continue_19 == "si" or continue_19_30 == "si" or continue_20 == "si":
                available_date = datetime.strptime(str(giorniAggiunti), '%Y-%m-%d').strftime('%d/%m/%y')

                text_link1 = str(centri[z]) + " - " + str(available_date) + " 19.00\n"
                text_link2 = str(centri[z]) + " - " + str(available_date) + " 20.00\n"
                text_link3 = str(centri[z]) + " - " + str(available_date) + " 19.30\n"

                url = str("<a href='https://www.prenotauncampo.it/default/search/payment/?fieldId=") + str(campi[z][i]) + str(
                    "&date=") + str(giorniAggiunti) + str(
                    "+19%3A00&duration=90&searched_time='>") + str(text_link1) + str("</a> ")
                url2 = str("<a href='https://www.prenotauncampo.it/default/search/payment/?fieldId=") + str(campi[z][i]) + str(
                    "&date=") + str(giorniAggiunti) + str(
                    "+20%3A00&duration=90&searched_time='>") + str(text_link2) + str("</a> ")
                url3 = str("<a href='https://www.prenotauncampo.it/default/search/payment/?fieldId=") + str(campi[z][i]) + str(
                    "&date=") + str(giorniAggiunti) + str(
                    "+19%3A30&duration=90&searched_time='>") + str(text_link3) + str("</a> ")


                # cerca campi alle 19

                if continue_19 == "si":
                    try:
                        elementCss1 = str(".h25:nth-child(1) > .text-center:nth-child(") + str(day(j)) + str(") > .tx--white")
                        click1 = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, elementCss1)))
                        driver.execute_script("arguments[0].click();", click1)  # to handle ElementClickInterceptedException
                    except NoSuchElementException as e:
                        continue_19 = "no"
                    except TimeoutException as e:
                        continue_19 = "no"

                    if continue_19 == "si":
                        try:
                            element19 = str(campi[z][i]) + "_19_00"
                            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, element19)))
                            WebDriverWait(driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '90min')]")))
                        except TimeoutException as e:
                            print('court %d not available on %s at 7pm' % (campi[z][i], giorniAggiunti))
                        except NoSuchElementException as e:
                            print('court %d not available on %s at 7pm' % (campi[z][i], giorniAggiunti))
                        else:
                            payload['text'] += url


                # cerca campi alle 19.30

                if continue_19_30 == "si":
                    try:
                        elementCss2 = str(".h25:nth-child(2) > .text-center:nth-child(") + str(day(j)) + str(") > .tx--white")
                        click2 = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, elementCss2)))
                        driver.execute_script("arguments[0].click();", click2)  # to handle ElementClickInterceptedException
                    except NoSuchElementException as e:
                        continue_19_30 = "no"
                    except TimeoutException as e:
                        continue_19_30 = "no"

                    if continue_19_30 == "si":
                        try:
                            element1930 = str(campi[z][i]) + "_19_30"
                            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, element1930)))
                            WebDriverWait(driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '90min')]")))
                        except TimeoutException as e:
                            print('court %d not available on %s at 7.30pm' % (campi[z][i], giorniAggiunti))
                        except NoSuchElementException as e:
                            print('court %d not available on %s at 7.30pm' % (campi[z][i], giorniAggiunti))
                        else:
                            payload['text'] += url3

                # cerca campi alle 20

                if continue_20 == "si":
                    try:
                        elementCss3 = str(".h25:nth-child(3) > .text-center:nth-child(") + str(day(j)) + str(") > .tx--white")
                        click3 = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, elementCss3)))
                        driver.execute_script("arguments[0].click();", click3)  # to handle ElementClickInterceptedException
                    except NoSuchElementException as e:
                        continue_20 = "no"
                    except TimeoutException as e:
                        continue_20 = "no"

                    if continue_20 == "si":
                        try:
                            element20 = str(campi[z][i]) + "_20_00"
                            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, element20)))
                            WebDriverWait(driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '90min')]")))
                        except TimeoutException as e:
                            print('court %d not available on %s at 8pm' % (campi[z][i], giorniAggiunti))
                        except NoSuchElementException as e:
                            print('court %d not available on %s at 8pm' % (campi[z][i], giorniAggiunti))
                        else:
                            payload['text'] += url2

requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN), data=payload)
driver.close()
print(datetime.now() - startTime)

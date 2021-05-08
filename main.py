from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd
from email.message import EmailMessage
import smtplib
from discord_webhook import DiscordWebhook


# Get the webpage source code
PATH = "/home/island/Downloads/chromedriver"
options = Options()
options.add_argument('--no-sandbox') # required
# options.add_argument('--headless') # for running on server
# chrome_options.add_argument('--disable-dev-shm-usage') # optional
driver = webdriver.Chrome(PATH,options=options)
driver.get('https://lom.agc.gov.my/subsid.php?type=pua')
time.sleep(5) # let page load
page_source = driver.page_source

# Parse the data
soup = BeautifulSoup(page_source, 'lxml')
driver.quit() # close the browser

#Get the first row PUA
pub_date = soup.findAll("td")[0].text
pu_number = soup.findAll("td")[1].text
title = soup.findAll("td")[2].text
status = soup.findAll("td")[3].text
commencement = soup.findAll("td")[5].text

#Get the PDF download link
first_link = soup.find_all('a', href=True)[23]
change_type = str(first_link['href'][9:])
remove_space = change_type.replace(" ", "%20")
dl_link = "https://lom.agc.gov.my/" + remove_space

#Check row 1 column 3 for the word keywords
words = title.split(" ")
for word in words:
    if word == "BERJANGKIT":
        df = pd.read_csv('/home/island/PycharmProjects/agc_v2/berjangkit.csv')
        old_pu_number = (df.iloc[0, 1])
        old_date = (df.iloc[0, 0])
        if pu_number == old_pu_number:
            print("no change")
            break

        else:
            msg = f"""
            
            DATE: {pub_date}

            TITLE: {title}

            PDF LINK: {str(dl_link)}

            STATUS: {status}

            COMMENCEMENT: {commencement}

            """
            # Send email
            # email = EmailMessage()
            # email.set_content(msg)
            # recipients = ['andrew@malaysiakini.com']
            # email['From'] = 'newsdesk.bot@malaysiakini.com'
            # email['To'] = ', '.join(recipients)
            # email['Subject'] = "TEST - Please ignore"
            #
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls()
            # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            # server.login('newsdesk.bot@malaysiakini.com', 'mkini@KINI2021')
            # server.send_message(email)
            # server.quit()
            #
            # # Execute webhook
            # webhook = DiscordWebhook(url='https://discord.com/api/webhooks/840641243884683304/xfB3k0tYH43PBDfgLexkqIPcz3qYht5zMLV5kh_eSRBCdS8RYV3vpeQ1L39k2-4yD5MI', content=msg)
            # response = webhook.execute()

            # Update the csv
            df2 = df.replace({
                'Number': {old_pu_number: pu_number},
                'Date': {old_date: pub_date},
            })  # replace old with new to df
            df2.to_csv('berjangkit.csv', index=False)  # write new df (pu_number) to csv
            break


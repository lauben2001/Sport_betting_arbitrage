# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:01:37 2023

@author: benja
"""

import pandas as pd
import numpy as np
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
from pretty_html_table import build_table

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
general_fee = 0
df_fees = pd.DataFrame(
      {"10x10bet": [general_fee],
        "1xBet": [general_fee],
        "Alphabet": [general_fee],
      "bet-at-home": [general_fee],
      "bet365": [general_fee],
      "bwin": [general_fee],
      "Curebet": [general_fee],
      "Coolbet": [general_fee],
      "GGBET": [general_fee],
      "Interwetten": [general_fee],
      "Lasbet": [general_fee],
      "Marathonbet": [general_fee],
      "Marsbet": [general_fee],
      "Pinnacle": [general_fee],    
      "Unibet": [general_fee],
      "VOBET": [general_fee],
      "William Hill": [general_fee],
      "William Hill": [general_fee],
      })
def mail_send(df_send):
    df = df_send
    recipients = ['ocipit_arbitrage@web.de'] 
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = "Arbitrage Alert"
    msg['From'] = 'ocipit_arbitrage@web.de'
    
    
    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(df.to_html())
    
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
        
    server = smtplib.SMTP('smtp.web.de', 587)
    server.connect('smtp.web.de', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("ocipit_arbitrage@web.de", "ArbitrageIn2023")
    
    server.sendmail(msg['From'], emaillist , msg.as_string())
    server.quit()
    print("Email sent")


  

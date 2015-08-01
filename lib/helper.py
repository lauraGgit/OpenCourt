import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(per, num, total, startTime):
    
    if num == 0:
        subject = "Volumes Scraped Starting Case Scraper"
        text = "There are " + str(total) + " cases to scrape started at " + str(startTime)
    else:
        subject = 'Your Script is through '+str(per)+ '% ('+str(num)+'/'+str(total)+ ') cases'
        text = "You are now "+str(per)+"% complete with the crawl start was started at "+  str(startTime)
    emailSend(subject, text)

def emailSend(subject, text, smtpserver=config.server):
    html = "<p>"+text+"</p>"
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    frm = config.frm_addr
    to_add = config.to_addr
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = frm
    message['To'] = ', '.join(to_add)
    message.attach(part1)
    message.attach(part2)
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(config.user, config.passw)
    problems = server.sendmail(frm, to_add, message.as_string())
    server.quit()
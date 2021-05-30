# -*- coding: utf-8 -*-

import smtplib
import threading
import email.message
from datetime import datetime

__all__ = ["SendEmail", "ThreadSendEmail"]

class SendEmail(object):
    def __init__(self, *args):
        self.server = "br666.hostgator.com.br"
        self.port = 465
        self.origin = "tester@dotpyc.com"
        self.password = "Dottes!@#2021"
        self.now = datetime.now()
    
    """ Function send email for client """
    def send(self, email_destiny, recovery_code):
        try:
            
            html = (f""" 
            <html>
                <head>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css">
                </head>
                <div class="title">
                <h3 style="margin: 10px;">
                    Olá {email_destiny}, o seu codigo de recuperação é:</h3></br>
                    <p><strong>{recovery_code}</strong></p>
                </div>
                <p style="margin: 10px;">{self.now.strftime('%d/%m/%y, %H:%M:%S')}</p>
            </html> """)

            msg = email.message.Message()
            msg['Subject'] = "Recuperação de conta Mattos.Upload"
            msg['From'] = self.origin
            msg['To'] = email_destiny
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(html, charset='utf-8')
            
            """ This instace for SMTP Server """
            server_smtp = smtplib.SMTP_SSL(self.server, self.port)
            
            """ Login Credentials for sending the mail """
            server_smtp.login(msg['From'], self.password)
    
            """ Send email """
            server_smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
                                                            
            """ Destroy connection """
            server_smtp.quit()

        except Exception as error:
            print("Error: ", error)
            return {"status": 404, "error": str(error)}
    
    def create_thread(self, email, code):
        self.thread = threading.Thread(target=self.send, args=[email, code])
        self.thread.daemon = True
        self.thread.start()

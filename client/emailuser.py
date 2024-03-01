import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup, Tag

from email.message import EmailMessage
import ssl
import smtplib


class EmailUser():
    def __init__(self, creds: dict):
        self._email_password = os.environ["EMAIL_PASSWORD"]
        self._soup = self.cook_soup(creds=creds)
        self._body = str(self._soup)

    @property
    def body(self) -> str:
        return self._body

    @property
    def email_password(self) -> str:
        return self._email_password

    @property
    def from_addr(self) -> str:
        return "blake@terminusgps.com"

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    @property
    def subject(self) -> str:
        return "Your Wialon Credentials"

    def create_message(self, to_addr: str) -> EmailMessage:
        msg = EmailMessage()
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg['Subject'] = self.subject
        msg.set_content(self.body, subtype="html")

        return msg

    def cook_soup(self, creds: dict) -> BeautifulSoup:
        with open("client/emailuser.html", "r") as html:
            soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")
            soup = self.fill_soup(soup=soup, creds=creds)

            return soup

    def fill_soup(self, soup: BeautifulSoup, creds: dict) -> BeautifulSoup:
            inputs: list[Tag] = soup.find_all("h2")
            inputs.extend(soup.find_all("a"))

            subs: list[tuple] = [("username", creds["email"]), ("password", creds["password"]), ("return_url", f"https://terminusgps.com/login?username={creds['email']}")]

            for index, input in enumerate(inputs):
                input.string = subs[index][1]

            return soup

    def send(self, to_addr: str) -> bool:
        msg = self.create_message(to_addr=to_addr)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.from_addr, self.email_password)
            server.sendmail(self.from_addr, to_addr, msg.as_string())
            return True
        return False

if __name__ == "__main__":
    load_dotenv()
    creds = {
        "email": "blake@terminusgps.com",
        "password": "AReallySecurePassword123!"
    }
    email = EmailUser(creds=creds)
    print(email.send(to_addr="blakenall@proton.me"))

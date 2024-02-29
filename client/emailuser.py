import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup, Tag

from email.message import EmailMessage
import ssl
import smtplib


class EmailUser():
    def __init__(self, data: dict):
        self._address = data["email"]
        self._email_password = os.environ["EMAIL_PASSWORD"]
        self._soup = self.cook_soup(data=data)
        self._body = str(self._soup)

    @property
    def from_addr(self) -> str:
        return "blake@terminusgps.com"

    @property
    def to_addr(self) -> str:
        return self._address

    @property
    def subject(self) -> str:
        return "Your Wialon Credentials"

    @property
    def body(self) -> BeautifulSoup:
        return self._body

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    @property
    def email_password(self) -> str:
        return self._email_password

    def send(self) -> bool:
        msg = EmailMessage()
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr
        msg['Subject'] = self.subject
        msg.set_content(self.body, subtype="html")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.from_addr, self.email_password)
            server.sendmail(self.from_addr, self.to_addr, msg.as_string())
            return True
        return False

    def cook_soup(self, data: dict) -> BeautifulSoup:
        with open("client/emailuser.html", "r") as html:
            soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")
            soup = self.fill_soup(soup=soup, data=data)

            return soup

    def fill_soup(self, soup: BeautifulSoup, data: dict) -> BeautifulSoup:
            inputs: list[Tag] = soup.find_all("h2")
            inputs.extend(soup.find_all("a"))

            subs: list[tuple] = [("username", data["username"]), ("password", data["password"]), ("return_url", f"https://terminusgps.com/login?username={data['username']}")]

            for index, input in enumerate(inputs):
                input.string = subs[index][1]

            return soup

if __name__ == "__main__":
    load_dotenv()
    data = {
        "email": "blake@terminusgps.com",
        "username": "blake@terminusgps.com",
        "password": "AReallySecurePassword123!"
    }
    email = EmailUser(data=data)
    print(email.send())

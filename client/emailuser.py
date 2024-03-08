import os
import smtplib
import ssl
from email.message import EmailMessage

from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
from smtplib import SMTPException


class EmailUser:
    def __init__(self, creds: dict) -> None:
        self._email_password: str = os.environ["EMAIL_PASSWORD"]
        self._soup: BeautifulSoup = self.cook_soup(creds=creds)
        self._body: str = str(self._soup)

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
        msg["From"] = self.from_addr
        msg["To"] = to_addr
        msg["Subject"] = self.subject
        msg.set_content(self.body, subtype="html")

        return msg

    def cook_soup(self, creds: dict[str, str]) -> BeautifulSoup:
        with open("client/emailuser.html", "r") as html:
            soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")
            return self.fill_soup(soup=soup, creds=creds)

    def fill_soup(self, soup: BeautifulSoup, creds: dict) -> BeautifulSoup:
        key: list[str] = ["Username: ", creds["email"], "Password: ", creds["password"]]
        inputs: list[Tag] = [tag for tag in soup.find_all("td")]

        for index, value in enumerate(inputs):
            value.string = key[index]

        return soup

    def send(self, to_addr: str) -> bool:
        msg = self.create_message(to_addr=to_addr)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(self.from_addr, self.email_password)
                server.sendmail(self.from_addr, to_addr, msg.as_string())
                _success = True

            except smtplib.SMTPException:
                _success = False

        return _success


if __name__ == "__main__":
    load_dotenv()
    creds = {"email": "blakenall@proton.me", "password": "AReallySecurePassword123!"}
    email = EmailUser(creds=creds)

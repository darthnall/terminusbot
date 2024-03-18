import smtplib
import ssl
from email.message import EmailMessage
from config import Config

from bs4 import BeautifulSoup

from dotenv import load_dotenv
from smtplib import SMTPException


class EmailUser:
    def __init__(self) -> None:
        self._email_password: str = Config.EMAIL_PASSWORD
        self._body: str

    @property
    def email_password(self) -> str:
        return self._email_password

    @property
    def from_addr(self) -> str:
        return "blake@terminusgps.com"

    @property
    def subject(self) -> str:
        return "Your Wialon Credentials"

    @property
    def body(self) -> str:
        return self._body

    def fill_soup(self, username: str, password: str) -> BeautifulSoup:
        with open("templates/emailuser.html") as f:
            soup = BeautifulSoup(f, "html.parser")

            username_tag = soup.find(id="username")
            password_tag = soup.find(id="password")
            login_link_tag = soup.find(id="login_link")

            username_tag.string = username
            password_tag.string = password
            login_link_tag['href'] = f"https://hosting.terminusgps.com/?user={username}"

        return soup

    def create_message(self, to_addr: str, soup: BeautifulSoup) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = self.from_addr
        msg["To"] = to_addr
        msg["Subject"] = self.subject
        msg.set_content(str(soup), subtype="html")

        return msg

    def send(self, to_addr: str, username: str, password: str) -> bool:
        soup = self.fill_soup(username=username, password=password)
        msg = self.create_message(to_addr=to_addr, soup=soup)

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
    email = EmailUser()
    email.send(to_addr="blakenall@proton.me", username="blakenall@proton.me", password="AReallySecurePassword!1")

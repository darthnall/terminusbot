import requests

class TestEndpoint:
    def __init__(self, name: str) -> None:
        self.name = name

class TestPost(TestEndpoint):
    def __init__(self, name: str) -> None:
        super().__init__(name)

if __name__ == "__main__":
    url = "http://localhost:5000/notify"
    data = {"unit": "867730050861750"}

    response = requests.post(url, json=data)
    print(response.text)

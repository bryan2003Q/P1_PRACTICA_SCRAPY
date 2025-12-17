from bs4 import BeautifulSoup

html = "<p>   Hola mundo   </p>"
soup = BeautifulSoup(html, "lxml")

print(soup.p.get_text())
print(soup.p.get_text(strip=True))

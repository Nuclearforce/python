from bs4 import BeautifulSoup
import requests
import csv 
i=1
location=[]
price=[]

for i in range(2):
    url = 'https://www.property24.com/for-sale/western-cape/9/p' + str(i)
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    for house in content.findAll('span', attrs={"class": "p24_location"}):
        location.append(house)
    for house in content.findAll('span', attrs={"class": "p24_price"}):
        price.append(house)

print(len(location))
print(len(price))


with open('property24.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["location", "price"])
    for i in range(len(price)):
        writer.writerow([location[i], price[i]])
     
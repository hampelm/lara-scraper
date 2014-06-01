from bs4 import BeautifulSoup
import csv
import os
import re

done = os.listdir('html')
done = sorted(done)

headers = ('name', 'address', 'status', 'status_date', 'date', 'resident_agent', 'assumed')
output = csv.DictWriter(open('out.csv', 'w'), headers)

for filename in done:
    f = open('html/' + filename, 'r')
    soup = BeautifulSoup(f.read())
    font_tags = soup.find_all('font')

    processed = {}
    processed["name"] = ''
    processed["address"] = ''
    processed["status"] = ''
    processed["status_date"] = ''
    processed["date"] = ''
    processed["resident_agent"] = ''
    processed["assumed"] = ''

    list = []

    for index, font in enumerate(font_tags):
        text = font.get_text()
        slimmed = ' '.join(text.split())

        if "Entity Name: " in slimmed:
            processed["name"] = slimmed[13:]
            list.append(slimmed[13:])

        if "Registered Office Address:" in slimmed and len(slimmed) > len("Registered Office Address:"):
            processed["address"] = slimmed[27:]
            list.append(slimmed[27:])

        if "Status: " in slimmed and len(slimmed) > len("Status:"):
            processed["status"] = slimmed.strip()[7:]
            processed["status_date"] = ""
            list.append(slimmed.strip()[7:])
            list.append("")

            if "Date" in slimmed:
                (status, statusDate) = slimmed.split("Date")
                processed["status"] = status.strip()[8:]
                processed["status_date"] = statusDate.strip()[2:]

                list.append(status.strip()[8:])
                list.append(statusDate.strip()[2:])

        if "Incorporation/Qualification Date:" in slimmed:
            date = font_tags[index + 1].get_text()
            slimmed = ' '.join(date.split())
            processed["date"] = slimmed
            list.append(slimmed)

        if "Resident Agent:" in slimmed:
            agent = font_tags[index + 1].get_text()
            slimmed = ' '.join(agent.split())
            processed["resident_agent"] = slimmed
            list.append(slimmed)

    links = soup.find_all("a", href=re.compile("adt_corp"))
    if links:
        processed["assumed"] = links[0]["href"]
        list.append(links[0]["href"])
    else:
        list.append("")

    output.writerow(processed)


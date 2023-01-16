# TODO
# 1. Make a request to the ebay.com and get a page
# 2. Collect data from each detail page
# 3. Collect all links to detail pages of each product
# 4. Write scraped data to a csv file
# reference: https://www.youtube.com/watch?v=m4hEAhHHykI

import requests
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    # title
    # price
    # item sold
    try:
        title = soup.find('h1', id='itemTitle').text.strip().replace(
            'Details about  \xa0', '')
    except:
        title = ''

    try:
        p = soup.find(
            'span', 'notranslate vi-VR-cvipPrice').text.strip()
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''

    try:
        condition = soup.find('div', class_='u-flL condText').text.strip()
    except:
        condition = ''

    features = {
        'title': title,
        'currency': currency,
        'price': price,
        'condition': condition
    }

    spec_keys = ['Processor',
                 'Screen Size',
                 'Color',
                 'RAM Size',
                 'SSD Capacity',
                 'GPU',
                 'Processor Speed',
                 'Brand',
                 'Series',
                 'Type',
                 'Maximum Resolution',
                 'Model',
                 'Operating System',
                 'Hard Drive Capacity',
                 'Storage Type',
                 'test']

    specs_len = len(soup.find_all(
        'div', class_='ux-labels-values__labels-content'))

    i = 1
    while i < specs_len:
        spec_label = soup.find_all(
            'div', class_='ux-labels-values__labels-content')[i].text.strip().replace(':', '')
        if spec_label in spec_keys:
            spec_value = soup.find_all(
                'div', class_='ux-labels-values__values-content')[i].text.strip()
            features[spec_label] = spec_value
        else:
            pass
        i += 1

        for spec in spec_keys:
            if spec not in features.keys():
                features[spec] = None
    print(features)
    return features


def main():
    url = 'https://www.ebay.com/itm/314323564719?hash=item492f24f8af:g:eXcAAOSwscZjwJrv&amdata=enc%3AAQAHAAAAkNU%2BBnk2P1b1WL%2FJIeWEAXRwNWP%2BPfISmfcxeuNu42xE18f7%2FyUhTJT8aRbAn1wUUMTLePIZsFYHCyR%2FDF90wZmoxWlzo%2F%2FNXCb0dw1d%2FgEAXPrQFdpa76ia8aLM5QBbQTXt6qcB3gffYYfh%2FBJYkpZHgoHBWUnLeFYwPNSbVwScUjeaVxhlLqOSFY49zPVmww%3D%3D%7Ctkp%3ABk9SR-Skoau2YQ'

    get_detail_data(get_page(url))


if __name__ == '__main__':
    main()

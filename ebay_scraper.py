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
            'Details about  ', '')
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

    detail_len = len(soup.find_all(
        'div', class_='ux-labels-values__labels-content'))

    i = 1
    specs = {}
    while i < detail_len:
        detail_label = soup.find_all(
            'div', class_='ux-labels-values__labels-content')[i].text.strip()
        detail_value = soup.find_all(
            'div', class_='ux-labels-values__values-content')[i].text.strip()
        specs[detail_label] = detail_value
        i += 1
    print(specs)

    # try:
    #     processor = soup.find_all(
    #         'div', class_='ux-labels-values__labels-content')[1].text.strip()
    # except:
    #     processor = ''

    print(title)
    print(currency)
    print(price)
    print(condition)


def main():
    url = 'https://www.ebay.com/itm/314323564719?hash=item492f24f8af:g:eXcAAOSwscZjwJrv&amdata=enc%3AAQAHAAAAkNU%2BBnk2P1b1WL%2FJIeWEAXRwNWP%2BPfISmfcxeuNu42xE18f7%2FyUhTJT8aRbAn1wUUMTLePIZsFYHCyR%2FDF90wZmoxWlzo%2F%2FNXCb0dw1d%2FgEAXPrQFdpa76ia8aLM5QBbQTXt6qcB3gffYYfh%2FBJYkpZHgoHBWUnLeFYwPNSbVwScUjeaVxhlLqOSFY49zPVmww%3D%3D%7Ctkp%3ABk9SR-Skoau2YQ'

    get_detail_data(get_page(url))


if __name__ == '__main__':
    main()

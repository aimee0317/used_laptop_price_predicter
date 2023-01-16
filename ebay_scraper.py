# TODO
# 1. Make a request to the ebay.com and get a page
# 2. Collect data from each detail page
# 3. Collect all links to detail pages of each product
# 4. Write scraped data to a csv file
# reference: https://www.youtube.com/watch?v=m4hEAhHHykI

import requests
from bs4 import BeautifulSoup
import csv


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    try:
        title = soup.find('h1', id='itemTitle').text.strip().replace(
            'Details about  \xa0', '')
    except:
        title = ''

    try:
        try:
            p = soup.find('span', 'notranslate vi-VR-cvipPrice').text.strip()
        except:
            p = soup.find('span', class_='notranslate',
                          id='prcIsum').text.strip()
        else:
            p = soup.find(
                'span', class_='notranslate vi-VR-cvipPrice').text.strip()
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
    return features


def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [item.get('href') for item in links]

    return urls


def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = list(data.values()) + [url]

        writer.writerow(row)


def main():
    pgn_max = 2
    pgn = 1
    while pgn <= pgn_max:
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptop&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=' + \
            str(pgn)
        products = get_index_data(get_page(url))
        products_work = products[1:]

        for link in products_work:
            data = get_detail_data(get_page(link))
            write_csv(data, link)
        pgn += 1


if __name__ == '__main__':
    main()

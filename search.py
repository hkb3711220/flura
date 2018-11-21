import requests
from bs4 import BeautifulSoup
import numpy as np
import urllib
import os
from PIL import Image

os.chdir(os.path.dirname(__file__))

class search(object):

    def __init__(self, target):

        self.path = '.\input'
        if os.path.exists(self.path) == False:
            os.mkdir(self.path)
        self.HEADER = {'User-Agent': 'Mozilla/5.0'}
        self.target = target
        self.res_text = self._reponse()
        self.product_full_names, self.std_prices, self.sale_prices, self.discount_rate = self._get_info()
        self.img_name = self._download_img()

    def _reponse(self):
        url = 'https://www.furla.com/us/en/eshop/search/?lang=default&q={}'.format(str(self.target))
        try:
            response = requests.get(url, headers = self.HEADER)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

        soup = BeautifulSoup(response.text, 'lxml')

        return soup

    def _get_info(self):

        #Get Product Name
        product_info = self.res_text.find_all('div', attrs={'class':'product-info'})
        product_names = [info.find('div', attrs={'class':'product-name'}).text.replace('\n', ' ').strip() for info in product_info]
        product_descripts =  [info.find('div', attrs={'class':'product-description'}).text.replace('\n', ' ').strip() for info in product_info]
        product_full_names = []
        for name, descript in zip(product_names, product_descripts):
            full_name = [name, descript]
            product_full_names.append(' '.join(full_name))

        #Get product_price
        divs = [info.find('div', attrs={'class':'product-pricing'}) for info in product_info]
        spans = [div.find_all('span') for div in divs]

        std_prices = []
        sale_prices = []
        for span in spans:
            std_price = span[0].text.replace('$', '')
            std_price = float(std_price)
            if span[1] is not None:
                sale_price = span[1].text.replace('$', '')
                sale_price = float(sale_price)
            std_prices.append(std_price)
            sale_prices.append(sale_price)

        if len(sale_prices) > 0:
            discount_rate = np.round(((np.array(std_prices) - np.array(sale_prices)) / np.array(std_prices)) * 100)

        return product_full_names, std_prices, sale_prices, discount_rate

    def _download_img(self):

        divs = self.res_text.find_all('div', attrs={'class':'product-image'})
        srcs = [div.a.img['src'] for div in divs]

        name = self.product_full_names[0].split(' ')
        name = '_'.join(name)

        img_name = []

        for i, src in enumerate(srcs):
            name = self.product_full_names[i].split(' ')
            name = '_'.join(name)
            save_path = os.path.join(self.path, name + '.png')
            img_name.append(name)
            if os.path.exists(save_path):
                continue
            else:
                urllib.request.urlretrieve(src, save_path)

        return img_name

#print(search(target='alba')._download_img())

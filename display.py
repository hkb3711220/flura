import sys
sys.path.append('./')

from search import search
import pandas as pd
from PIL import Image
from io import BytesIO
from IPython.display import HTML
import os
import base64
import webbrowser

os.chdir(os.path.dirname(__file__))
result = search(target='alba')
pd.set_option('display.max_colwidth', -1)

class display(object):

    def __init__(self):
        self.path = './display'
        if os.path.exists(self.path) == False:
            os.mkdir(self.path)
        self.html = os.path.join(self.path, 'display.html')
        self.mk_df()
        webbrowser.open(self.html, new=0)

    def mk_df(self):

        df = pd.DataFrame()
        df['Product Name'] = result.product_full_names
        df['Standard Price'] = result.std_prices
        df['Sale Price'] = result.sale_prices
        df['Discount Rate'] = result.discount_rate
        df['Image'] = [self.get_thumbnail(name) for name in result.img_name]

        return df.to_html(self.html, formatters={'Image': self.image_formatter}, escape=False)

    def get_thumbnail(self, name):

        path = os.path.join(os.path.dirname(__file__), 'input', name + '.png')
        i = Image.open(path)
        i.thumbnail((150, 150), Image.LANCZOS)

        return i

    def image_base64(self, im):
        if isinstance(im, str):
            im = get_thumbnail(im)
        with BytesIO() as buffer:
            im.save(buffer, 'jpeg')
            return base64.b64encode(buffer.getvalue()).decode()

    def image_formatter(self, im):
        return f'<img src="data:image/jpeg;base64,{self.image_base64(im)}">'

display()

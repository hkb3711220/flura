import sys
from itchat.content import *
sys.path.append('./')

import itchat
from search import search
import numpy as np
import os

itchat.auto_login(hotReload=True)

class send(object):

    def __init__(self, result):

        self.author = itchat.search_friends()
        self.product_name = result.product_full_names
        self.discount_rate = result.discount_rate
        self.img_name = result.img_name
        self.hrefs = result.hrefs
        self.base_discount_rate = float(15)
        self.msg_product, self.msg_dic_rate, self.msg_href, self.msg_img_name = self._pick_up()
        self._send_msg()

    def _pick_up(self):

        inds = np.where(self.discount_rate > self.base_discount_rate)[0]
        msg_product = [self.product_name[i] for i in inds]
        msg_dic_rate = [self.discount_rate[i] for i in inds]
        msg_href = [self.hrefs[i] for i in inds]
        msg_img_name =  [self.img_name[i] for i in inds]

        return msg_product, msg_dic_rate, msg_href, msg_img_name

    def _send_msg(self):
        for i, j, k, l in zip(self.msg_product, self.msg_dic_rate, self.msg_href, self.msg_img_name):
            msg_str = "ENJOY %s OFF ON %s, PLEASE CHECK URL: %s" % (str(int(j)) +'%', i, k)
            path = os.path.join(os.path.dirname(__file__), 'input', l + '.png')
            self.author.send(msg_str)
            self.author.send_image(path)

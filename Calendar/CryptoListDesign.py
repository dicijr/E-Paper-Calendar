from DesignEntity import DesignEntity
from TableDesign import TableDesign
from Assets import defaultfontsize
from CryptoPrices import CryptoPrices
from settings import crypto_coins as cryptos


class CryptoListDesign (DesignEntity):
    def __init__ (self, size, coin, text_size = defaultfontsize):
        super(CryptoListDesign, self).__init__(size)
        self.coin = coin
        self.__post_matrix__ = [[]]
        self.text_size = text_size

    def __finish_image__ (self):
        self.__fill_post_matrix__()
        table_design = TableDesign(self.size, line_spacing=2, col_spacing=3, matrix=self.__post_matrix__, fontsize = self.text_size, mask=False, wrap=True, truncate_rows=True)
        self.draw_design(table_design)

    def __fill_post_matrix__ (self):
        prices, coins = CryptoPrices.__get_prices__(self.coin)
        for price, coin in zip(prices, coins):
            row = coin + ": $" + str(price)
            self.__post_matrix__[0].append(row)

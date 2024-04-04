


class Symbol(object):
    # 定义使用的sh大盘
    SH_INDEX = ['000001', '000300']

    SZ_INDEX = ['399001', '399005', '399006']


    def __init__(self, market, sub_market, symbol_code):
        if isinstance(market, EMarketTargetType) and isinstance(sub_market, ESubMarketTargetType):
            self._market = market
            self._sub_market = sub_market
            self._symbol_code = symbol_code
            self.source = None
        else:  
            raise TypeError("market and sub_market must be EMarketTargetType and ESubMarketTargetType object")
        

    def __str__(self):
        return '{}_{}_{}'.format(self._market, self._sub_market, self._symbol_code)
    

    # todo 为什么要重写__repr__方法
    __repr__ = __str__


    def __len__(self):
        m_symbol = '{}_{}_{}'.format(self._market, self._sub_market, self._symbol_code)
        return len(m_symbol)
    

    



    


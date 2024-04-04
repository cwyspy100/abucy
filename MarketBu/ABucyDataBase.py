

"""数据源基础市场基类"""
class BaseMarket(object):

    def __init__(self, symbol):
        if not isinstance(symbol, Symbol):
            raise TypeError("symbol must be Symbol object")
        
        self._symbol = symbol

    
    

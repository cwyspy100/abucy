

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels import api as sm, regression
import seaborn as sns



def calc_regress_deg(y, show=True):
    """
    将y值 zoom到与x一个级别，之后再fit出弧度转成角度
    1 多个股票的趋势比较提供量化基础，只要同一个时间范围，就可以比较
    2 接近视觉感受到的角度
    :param y:  可迭代序列
    :param show: 是否可视化结果
    :return: deg角度float值
    """
    # 将y值 zoom到与x一个级别
    model, _ = regress_y(y, mode=True, zoom=True, show=show)
    rad = model.params.iloc[1]
    # fit出弧度转成角度
    deg = np.rad2deg(rad)
    return deg


def regress_xy(x, y, mode=True, zoom=False, show=False):
    """
    使用statsmodels.regression.linear_model进行简单拟合操作，返回model和y_fit
    :param x: 可迭代序列
    :param y: 可迭代序列
    :param mode: 是否需要mode结果，在只需要y_fit且效率需要高时应设置False, 效率差异：
                 mode=False: 1000 loops, best of 3: 778 µs per loop
                 mode=True:  1000 loops, best of 3: 1.23 ms per loop
    :param zoom: 是否缩放x,y
    :param show: 是否可视化结果
    :return: model, y_fit, 如果mode=False，返回的model=None
    """
    if zoom:
        # 将y值 zoom到与x一个级别，不可用ABuScalerUtil.scaler_xy, 因为不管x > y还y > x都拿 x.max() / y.max()
        # TODO ABuScalerUtil中添加使用固定轴进行缩放的功能
        zoom_factor = x.max() / y.max()
        y = zoom_factor * y

    if mode:
        # 加常数1列
        x = sm.add_constant(x)
        model = regression.linear_model.OLS(y, x).fit()

        intercept = model.params.iloc[0]
        rad = model.params.iloc[1]
        # y = kx + b, x取x[:, 1]，因为add_constant
        y_fit = x[:, 1] * rad + intercept
    else:
        # noinspection PyCallingNonCallable
        y_fit = np.polynomial.Chebyshev.fit(x, y, 1)(x)
        model = None
    if show:
        with plt_show():
            # 取-1因为有OLS add_constant和Chebyshev没有add_constant的两种情况
            x_plot = x[:, -1]
            # 绘制x， y
            plt.plot(x_plot, y)
            # 绘制x， 拟合的y
            plt.plot(x_plot, y_fit)

        with plt_show():
            # 再使用sns绘制，对比拟合结果
            sns.regplot(x=x_plot, y=y)
    return model, y_fit


def plt_show():
    """
        在conda5.00封装的matplotlib中全局rc的figsize在使用notebook并且开启直接show的模式下
        代码中显示使用plt.show会将rc中的figsize重置，所以需要显示使用plt.show的地方，通过plt_show
        上下文管理器进行规范控制：
        1. 上文figsize设置ABuEnv中的全局g_plt_figsize
        2. 下文显示调用plt.show()
    """
    plt.figure(g_plt_figsize=(14,17))
    yield
    plt.show()



def regress_y(y, mode=True, zoom=False, show=False):
    """
    使用statsmodels.regression.linear_model进行简单拟合操作, 参数中只提供y序列，
    x使用np.arange(0, len(y))填充
    :param y: 可迭代序列
    :param mode: 是否需要mode结果，在只需要y_fit且效率需要高时应设置False, 效率差异：
             mode=False: 1000 loops, best of 3: 778 µs per loop
             mode=True:  1000 loops, best of 3: 1.23 ms per loop
    :param zoom: 是否缩放x,y
    :param show: 是否可视化结果
    :return: model, y_fit, 如果mode=False，返回的model=None
    """
    x = np.arange(0, len(y))
    return regress_xy(x, y, mode=mode, zoom=zoom, show=show)
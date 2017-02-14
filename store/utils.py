from decimal import Decimal as bDecimal


def Decimal(data):
    return bDecimal(data).quantize(bDecimal('0.00'))


def quantize(decimal_data):
    return decimal_data.quantize(bDecimal('0.00'))

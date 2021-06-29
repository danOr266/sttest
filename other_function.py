import decimal as dl






def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += dl.Decimal(jump)
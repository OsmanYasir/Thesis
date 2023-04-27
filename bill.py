class Bill:
    def __init__(self,filename, amount, period, paymentid, organization):
        self.fileName = filename
        self.amount = amount
        self.paymentid = paymentid
        self.organization = organization
        self.period = period

    def __str__(self):
        return f"Bill(amount={self.amount}, paymentid={self.paymentid}, organization='{self.organization}, period='{self.period}'')"
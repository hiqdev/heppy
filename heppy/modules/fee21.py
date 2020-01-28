from fee import fee

class fee21(fee):
    def __init__(self, xmlns):
        fee.__init__(self, xmlns)
        self.name = 'fee'


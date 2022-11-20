class Outervariables:
    defvar = ''
    def __init__(self, results='РЕЗАЛТПУСТО', city='СИТИПУСТО'):
        self.results = results
        self.city = city
        self.defvar = city

    def display_info(self):
        print(self.city, self.results)



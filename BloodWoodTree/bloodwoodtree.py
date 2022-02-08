# 8 bloodwood trees total, 5 locked behind requirements
# 5 trees have an average of 1-5 logs (no modifier)
# 3 trees have an average of 5-7
# all trees have a minimum of 1 log

import math
from Daily.daily import Daily

from Resources.util import retrieve_item, price_to_int, price_to_str
from Resources.Modifiers import Woodcutting
#TODO: implement modifiers

class Bloodwoodtree(Daily):
    def __init__(self) -> None:
        super().__init__()
        self.modifier = 1.00
        self.base_min = 80
        self.base_max = 410
        #TODO: separate woodcutting formula into it's own class
        #Specific low and high of crystal hatchet
        self.low = 23
        self.high = 170
        self.level = 99
        self.success_percentage = 0
        self.item = retrieve_item("Bakriminel bolts", 3)    # category 3 is bolts
    
    def apply_modifer(self):
        # 4 different types of modifers, level modifier, low chance, high chance, both low and high
        self.high *= Woodcutting["Nature sentinel outfit"]
        self.high *= Woodcutting["Legendary lumberjack aura"]
        return

    def rawroll(self):
        roll = int(((99 - self.level) * self.low) + ((self.level - 1) * self.high) / 98)    # default is to floor the function
        self.success_percentage = roll/256
        return

    def calculate_probability(self):
        failure = (1 - (1 - self.success_percentage))
        # Something something 68% one standard deviation?
        n = int(math.log(0.32)/math.log(failure))
        
        # n = amount of logs chopped until we fail a roll and risk depleting the tree with a 1/4 chance
        total_logs = (n*3)*8    #this if flawed since not all bloodwood trees have the same depletion rate (wilderness)
        return total_logs

    def display_profit(self):
        self.apply_modifer()
        self.rawroll()
        logs = self.calculate_probability()
        price = price_to_int(self.item['current']['price']) * 10    # 10 bolt per log
        print("\nTotal logs estimated: ", logs)
        print("Profit: ", price_to_str(logs * price))
        print("Wilderness - 3 trees\tArdougne farming patch\tSouls Wars\tRitual Plateau\tDarkmeyer\tGorajo resource dungeon")
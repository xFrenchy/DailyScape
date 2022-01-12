# 8 bloodwood trees total, 5 locked behind requirements
# 5 trees have an average of 1-5 logs (no modifier)
# 3 trees have an average of 5-7
# all trees have a minimum of 1 log

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
        self.item = retrieve_item("Bakriminel bolts", 3)    # category 3 is bolts
    
    def apply_modifer(self):
        # the only modifier to actually boost the yield comes from Resourceful aura and Refined perk
        pass


    def display_profit(self):
        price = price_to_int(self.item['current']['price'])
        print("\n###\tModifiers not implemented yet\t###\nBase max profit: ", price_to_str(self.base_max * price))
        print("Base min profit: ", price_to_str(self.base_min * price))
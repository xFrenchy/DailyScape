import locale   # to convert numbers from string to int with comma

from Resources.util import retrieve_item, G_RUNE_CATEGORY, price_to_str

G_SHOP_RUNE_PRICE = {"Air rune": 17, "Water rune": 17, "Earth rune": 17, "Fire rune": 17, "Mind rune": 17, "Body rune": 16, 
"Chaos rune": 140, "Nature rune": 372, "Death rune": 310, "Law rune": 378, "Blood rune": 550, "Soul rune": 410, "Astral rune": 220, "Cosmic rune": 232}

class Shop:
    def __init__(self) -> None:
        self.name = ""
        self.location = ""
        self.teleport = ""
        self.inventory = {}
        self.total_profit = 0
        self.individual_profit = []
    
    def __init__(self, name, location, teleport, inventory):
        self.name = name
        self.location = location
        self.teleport = teleport
        self.inventory = inventory
        self.total_profit = 0
        self.individual_profit = []
    
    def calculate_profit(self):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        for item_name, stock in self.inventory.items():
            price = 0
            rune = retrieve_item(item_name, G_RUNE_CATEGORY)
            try:
                price = locale.atoi(rune['current']['price']) * stock
            except AttributeError:
                price = rune['current']['price'] * stock
            cost = G_SHOP_RUNE_PRICE[item_name] * stock
            profit = (price - cost)
            self.total_profit += profit
            self.individual_profit.append(profit)
    
    def print(self):
        print(self.name, "\t", self.location, "\t", self.teleport, "\t", price_to_str(self.total_profit))
        sorted_runes = {}
        i = 0
        for rune_name, stock in self.inventory.items():
            sorted_runes[self.individual_profit[i]] = rune_name
            i += 1
        result = dict(sorted(sorted_runes.items(), key=lambda item: item[0], reverse=True))
        for profit, name in result.items():
            print(name, ": ", price_to_str(profit), "\t", end="")
        print("\n") # 2 new line


class RuneShopRun:
    def __init__(self) -> None:
        self.rune_shops = [
            Shop("Baba Yaga", "Lunar Isle", "Home Teleport", {"Air rune": 1000, "Water rune": 1000, "Earth rune": 1000, "Fire rune": 1000, "Mind rune": 1000, "Body rune": 1000, "Chaos rune": 300, "Nature rune": 300, "Death rune": 300, "Law rune": 100, "Blood rune": 100, "Soul rune": 100, "Astral rune": 100}),
            Shop("Magic Guild", "Yanille", "Home Teleport", {"Air rune": 1000, "Water rune": 1000, "Earth rune": 1000, "Fire rune": 1000, "Mind rune": 1000, "Body rune": 1000, "Chaos rune": 300, "Nature rune": 300, "Death rune": 1000, "Law rune": 100, "Blood rune": 100, "Soul rune": 100}),
            Shop("Ali's Discount", "Al Kharid", "Home Teleport", {"Air rune": 300, "Water rune": 300, "Earth rune": 300, "Fire rune": 300, "Nature rune": 300, "Law rune": 300, "Chaos rune": 300, "Death rune": 100, "Mind rune": 300, "Body rune": 300, "Blood rune": 100, "Cosmic rune": 300, "Soul rune": 100}),
            Shop("Battle Runes", "Wilderness near Edgeville", "Wilderness sword", {"Fire rune": 1000, "Water rune": 1000, "Air rune": 1000, "Earth rune": 1000, "Mind rune": 1000, "Chaos rune": 300, "Death rune": 100, "Blood rune": 100}),
            Shop("Lundail's Arena-side", "Mage Arena", "Edgeville teleport lever", {"Fire rune": 1000, "Water rune": 1000, "Air rune": 1000, "Earth rune": 1000, "Mind rune": 1000, "Body rune": 1000, "Nature rune": 300, "Chaos rune": 300, "Law rune": 100, "Cosmic rune": 100, "Death rune": 300}),
            Shop("Void Knight", "Void Knights' Outpost", "Ship from Port Sarim", {"Fire rune": 1000, "Water rune": 1000, "Air rune": 1000, "Earth rune": 1000, "Mind rune": 1000, "Body rune": 1000, "Chaos rune": 300, "Death rune": 100}),
            Shop("Tutab's Magical Market", "Ape Atoll", "Ape Atoll Teleport + greegree", {"Fire rune": 1000, "Water rune": 1000, "Air rune": 1000, "Earth rune": 1000, "Law rune": 100}),
            Shop("Carwen Essenbinder", "Burthorpe", "Home teleport", {"Fire rune": 300, "Water rune": 300, "Air rune": 300, "Earth rune": 300, "Mind rune": 100, "Body rune": 100, "Chaos rune": 30, "Death rune": 10}),
            Shop("Aubury", "Varrock", "Home teleport", {"Fire rune": 300, "Water rune": 300, "Air rune": 300, "Earth rune": 300, "Mind rune": 100, "Body rune": 100, "Chaos rune": 30, "Death rune": 10}),
            Shop("Betty", "Port Sarim", "Home Teleport", {"Fire rune": 300, "Water rune": 300, "Air rune": 300, "Earth rune": 300, "Mind rune": 100, "Body rune": 100, "Chaos rune": 30, "Death rune": 10}),
            Shop("Rune Store Assistant", "Anachronia", "Home Telepoort", {"Fire rune": 300, "Water rune": 300, "Air rune": 300, "Earth rune": 300, "Mind rune": 100, "Body rune": 100, "Chaos rune": 30, "Death rune": 10})
        ]

    def display(self):
        #calculate profit for each shop
        for shop in self.rune_shops:
            shop.calculate_profit()
        # sort shops based on profit
        self.rune_shops.sort(key=lambda x: x.total_profit, reverse=True)
        # display shop information
        print("\nBuying runes: ")
        for shop in self.rune_shops:
            shop.print()
        pass

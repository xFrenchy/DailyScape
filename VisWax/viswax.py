import requests
import locale   # to convert numbers from string to int with comma
from logging import raiseExceptions
from requests.api import request
from os.path import exists
from datetime import date, timedelta, datetime

from Daily.daily import Daily
from Resources.util import price_to_int, api_url, price_to_str, retrieve_item
from Resources.GID_Historic import GID_Historic1, GID_Historic2
from Resources.GID import GID
from Resources.GID_Generated_Historic import GID_generated

G_RUNE_CATEGORY = 32    # category 32 is 'Runes, Spells and Teleports' for API request

class RuneInfo:
    def __init__(self) -> None:
        self.name = ""
        self.GID = -1
        self.price = -1

class RuneSlot:
    def __init__(self) -> None:
        self.max_viswax = RuneInfo()
        self.max_profit = RuneInfo()

class Viswax(Daily):
    def __init__(self) -> None:
        super().__init__()
        self.price = 0
        self.GID_dict = {}
        self.GID_historic = []
        self.GID_historic2 = []
        self.relative_file_path = "../Resources/"
        self.GID_generated = []
        self.slot1 = RuneSlot()
        self.slot2 = [RuneSlot(), RuneSlot(), RuneSlot()]
        self.slot3 = RuneSlot()

    # Makes an HTTP Get request to the runescape wiki to retrieve Viswax information
    def get_viswax(self):
        """As of Nov 2021, viswax is on page 2 so that will be our starting point"""
        found = False
        rollover = False
        page = 2
        while found != True:
            #TODO: error proof response from timeouts and other things that would make my code oopsie woopsie
            response = requests.get(api_url + "items.json?category=0&alpha=v&page=" + str(page))
            
            if len(response.json()['items']) == 0:
                # items are empty, we have exhausted the list, reset page number to check everything before 2
                page = 0
                rollover = True
            else:
                # Search result for Viswax
                for item in response.json()['items']:
                    if item['name'] == 'Vis wax':
                        self.price = price_to_int(item['current']['price'])
                        found = True
                        break
            page += 1
            
            if rollover:
                assert page != 2, "Failed to find viswax from get request, exhausted every page"

    # Initializes the GID_Dict list and checks that it's at least length 20
    def load_GID(self):
        self.GID_dict = GID
        assert len(self.GID_dict) == 20
        
    # Initializes the GID_Historic list and checks that it's at least length 41
    def load_historic(self):
        self.GID_historic = GID_Historic1
        self.GID_historic2 = GID_Historic2
        # We have to check 40 days and 41 days in the past relative to today to predict future GID slot 1s
        if len(self.GID_historic) < 41 or len(self.GID_historic2) < 41:
            return False
        return True
    
    # Initializes the GID_Historic list and checks that it's at least length 41
    def load_generated_historic(self):
        self.GID_generated = GID_generated
        # We have to check 40 days and 41 days in the past relative to today to predict future GID slot 1s
        if len(self.GID_generated) < 41:
            return False
        return True

    # Function generates a list of predicted GID of slot 1 from 2021-03-28 until present + 1 month ahead
    def generate_historic(self):
        """This function will attempt at predicting the first slots to maximize the reward from vis wax
            https://www.reddit.com/r/runescape/comments/me9gnt/predicting_the_rune_goldberg_machine/
            Slot 1 is highly predictable (soul GID 20 can never be slot 1)
            Slot 2 is guessable
            Slot 3 is unpredictable
            
            Requirements:
            Function requires that the GID_Historic is loaded, or can be loaded. Otherwise it errors"""
        if not self.load_historic():
            raise FileNotFoundError("Failed to load from GID_Historic file") 

        day = 6
        month = 1
        year = 2022
        start = date(year, month, day)
        future = date.today() + timedelta(days=31)

        f = open("Resources/GID_Generated_Historic.py", "w")
        f.write("GID_generated = {\n")

        while start != future:
            # Slot 1 prediction
            difference = self.GID_historic[date.isoformat(start - timedelta(days=40))] - self.GID_historic[date.isoformat(start - timedelta(days=41))]
            today_GID = (self.GID_historic[date.isoformat(start - timedelta(days=1))] + difference) % 19

            #TODO: I feel like a proper dumbass for this line, brain too small right now to fix it
            if today_GID == 0:
                today_GID = 19
            
            assert today_GID > -1, "predicted GID is negative!"
            assert today_GID < 20, "predicated GID is out of range!"

            self.GID_historic[date.isoformat(start)] = today_GID

            # Slot 2 prediction
            old_gid = self.GID_historic2[date.isoformat(start - timedelta(days=40))]
            new_gid = [0,0,0]

            difference = [4, -1, 9]
            for i in range(3):
                val = (old_gid[i] + difference[i]) % 19
                # dummy brain action time again
                if val == 0:
                   val = 19

                if val == self.GID_historic[date.isoformat(start)]:
                    val = (val + 1) % 21    # not mod 19, this is the ONLY time it can be GID 20

                # dummy brain action time again
                if val == 0:
                   val = 19
                new_gid[i] = val

            self.GID_historic2[date.isoformat(start)] = new_gid

            # Attach GID to date, move forward
            f.write('"' + start.isoformat() + '" : [' + str(today_GID) + ", " + str(new_gid) + "],\n")
            
            day += 1
            try:
                start = date(year, month, day)
            except ValueError:
                try: # day out of range, increment month
                    day = 1
                    month += 1
                    start = date(year, month, day)
                except ValueError: # month out of range, increment year
                    day = 1
                    month = 1
                    year += 1
                    start = date(year, month, day)
        f.write("}\n")
        f.close()

    def update_generated_historic(self):
        #TODO: do this :)
        raise NotImplementedError("Programmer doesn't want to implement this function yet")
    
    # Function that predicts the first rune slot for max viswax and max profit
    def predict_first_slot(self):
        str_today = date.isoformat(datetime.utcnow().date())
        try:
            self.slot1.max_viswax.GID = self.GID_generated[str_today][0]
            #TODO: max profit can't be calculated until I find a way to predict what the hiearchy is, aka which runes have a value of 30 and then 29 etc
        except KeyError:
            #TODO
            #self.update_generated_historic()   # When this function is implemented, call it lol
            self.generate_historic()    # This function works as well but it generated from all the way back in March 2021, less effecient
            # file is regenerated, need to reassign GID_generated again, this will all be taken care of in the update_generated_historic I swear
            from Resources.GID_Generated_Historic import GID_generated
            self.load_generated_historic()
            self.slot1.max_viswax.GID = self.GID_generated[str_today]
        self.slot1.max_viswax.name = self.GID_dict[self.slot1.max_viswax.GID]["name"]
        rune = retrieve_item(self.slot1.max_viswax.name + " rune", G_RUNE_CATEGORY)    
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        try:
            self.slot1.max_viswax.price = locale.atoi(rune['current']['price']) * self.GID_dict[self.slot1.max_viswax.GID]["base"]
        except AttributeError:
            self.slot1.max_viswax.price = rune['current']['price'] * self.GID_dict[self.slot1.max_viswax.GID]["base"]
        #TODO: calculate first slot max profit

    def predict_second_slot(self):
        str_today = date.isoformat(datetime.utcnow().date())
        try:
            gid_list = self.GID_generated[str_today][1]
            self.slot2[0].max_viswax.GID = gid_list[0]
            self.slot2[1].max_viswax.GID = gid_list[1]
            self.slot2[2].max_viswax.GID = gid_list[2]
        except KeyError:
            #TODO
            #self.update_generated_historic()   # When this function is implemented, call it lol
            pass
        self.slot2[0].max_viswax.name = self.GID_dict[self.slot2[0].max_viswax.GID]["name"]
        self.slot2[1].max_viswax.name = self.GID_dict[self.slot2[1].max_viswax.GID]["name"]
        self.slot2[2].max_viswax.name = self.GID_dict[self.slot2[2].max_viswax.GID]["name"]
        rune1 = retrieve_item(self.slot2[0].max_viswax.name + " rune", G_RUNE_CATEGORY)
        rune2 = retrieve_item(self.slot2[1].max_viswax.name + " rune", G_RUNE_CATEGORY)
        rune3 = retrieve_item(self.slot2[2].max_viswax.name + " rune", G_RUNE_CATEGORY)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        try:
            self.slot2[0].max_viswax.price = locale.atoi(rune1['current']['price']) * self.GID_dict[self.slot2[0].max_viswax.GID]["base"]
        except AttributeError:
            self.slot2[0].max_viswax.price = rune1['current']['price'] * self.GID_dict[self.slot2[0].max_viswax.GID]["base"]
        try:
            self.slot2[1].max_viswax.price = locale.atoi(rune2['current']['price']) * self.GID_dict[self.slot2[1].max_viswax.GID]["base"]
        except AttributeError:
            self.slot2[1].max_viswax.price = rune2['current']['price'] * self.GID_dict[self.slot2[1].max_viswax.GID]["base"]
        try:
            self.slot2[2].max_viswax.price = locale.atoi(rune3['current']['price']) * self.GID_dict[self.slot2[2].max_viswax.GID]["base"]
        except AttributeError:
            self.slot2[2].max_viswax.price = rune3['current']['price'] * self.GID_dict[self.slot2[2].max_viswax.GID]["base"]
        #TODO: calculate first slot max profit
        pass

    def predict_third_slot(self):
        self.slot3.max_viswax.name = "?"
        self.slot3.max_viswax.price = "?"

    def cheap_attempts(self):
        """This function will give the user some options of which runes to try
        Assuming that slot 1 and slot 2 are too expensive"""
        options = {}
        #TODO: Optimize this loop, having 20 API calls really slows it down
        for key, value in self.GID_dict.items():
            # look up price from the name
            rune_resp = retrieve_item(value['name'] + " rune", G_RUNE_CATEGORY)
            # base * price = total
            try:
                options[value['name']] = int(locale.atoi(rune_resp['current']['price']) * value['base'])
            except AttributeError:
                options[value['name']] = int(rune_resp['current']['price'] * value['base'])
        
        # Sort on from least to greatest 
        result = dict(sorted(options.items(), key=lambda item: item[1]))
        iter = 0
        for key, value in result.items():
            print(key + " - " + price_to_str(value))
            iter += 1
            if iter >= 11:
                break
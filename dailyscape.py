from sympy import BlockDiagMatrix

from Resources.util import price_to_str

from VisWax.viswax import Viswax
from BloodWoodTree.bloodwoodtree import Bloodwoodtree
from Shop.RuneShop import RuneShopRun

if __name__ == '__main__':
    print("Welcome to DailyScape, here are today's calculations: ")

#Vis wax
    viswax_obj = Viswax()
    viswax_obj.get_viswax()
    print("Viswax gross profit: " + price_to_str(viswax_obj.price * 100))
    viswax_obj.load_GID()
    if not viswax_obj.load_generated_historic():
        print("Generated historic not detected. Let me generate that for you :}\n")
        viswax_obj.generate_historic()
    # If we are here, generated historic is guaranteed to exists, let's load it
    viswax_obj.load_generated_historic()
    viswax_obj.predict_first_slot()
    viswax_obj.predict_second_slot()
    viswax_obj.predict_third_slot()
    print("\nMax viswax")
    print("Slot 1: ", viswax_obj.slot1.max_viswax.name, "\tTotal: ", price_to_str(viswax_obj.slot1.max_viswax.price))
    print("Slot 2: ", viswax_obj.slot2[0].max_viswax.name, "\tTotal: ", price_to_str(viswax_obj.slot2[0].max_viswax.price),
    "\n        ", viswax_obj.slot2[1].max_viswax.name, "\tTotal: ", price_to_str(viswax_obj.slot2[1].max_viswax.price),
    "\n        ", viswax_obj.slot2[2].max_viswax.name, "\tTotal: ", price_to_str(viswax_obj.slot2[2].max_viswax.price))
    print("Slot 3: ", viswax_obj.slot3.max_viswax.name, "\tTotal: ", viswax_obj.slot3.max_viswax.price, "\t Use your runecrafting skillcape if you have it :)\n")
    print("If the above runes are too expensive, try out these recommendations")
    viswax_obj.cheap_attempts()

#Bloodwood tree
    bloodwood_obj = Bloodwoodtree()
    bloodwood_obj.display_profit()

#Rune Shop
    runeshop_obj = RuneShopRun()
    runeshop_obj.display()
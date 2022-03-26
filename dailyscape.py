from functools import partial
import tkinter as tk

from Resources.util import price_to_str

from VisWax.viswax import Viswax
from BloodWoodTree.bloodwoodtree import Bloodwoodtree
from Shop.RuneShop import RuneShopRun

if __name__ == '__main__':
    print("Welcome to DailyScape, here are today's calculations: ")
    viswax_obj = Viswax()
    bloodwood_obj = Bloodwoodtree()
    runeshop_obj = RuneShopRun()
    root = tk.Tk()
    root.title("DailyScape")
    '''
    Widgets are added here
    '''
    viswax_button = tk.Button(root, text="Viswax", width=25, activeforeground='DarkOrchid2', activebackground='DarkOrchid4', command=partial(viswax_obj.display, root))
    viswax_button.pack()

    exit_button = tk.Button(root, text="Exit", width=25, bg='indian red', command=root.destroy)
    exit_button.pack()
    root.mainloop()

#Bloodwood tree
    
    bloodwood_obj.display_profit()

#Rune Shop
    
    runeshop_obj.display()
import tkinter as tk
from gui import RentalAppGUI

def main():
    root = tk.Tk()
    app = RentalAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

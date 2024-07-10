import tkinter as tk
from gui import SecureDataHubApp
from ttkthemes import ThemedTk

if __name__ == "__main__":
    root = ThemedTk(theme="clam")
    app = SecureDataHubApp(root)
    root.mainloop()

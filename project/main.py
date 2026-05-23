from app import App
from PIL import ImageTk

if __name__ == "__main__":
    app = App()

    icon = ImageTk.PhotoImage(file="Icon.png")
    app.iconphoto(True, icon)

    app.mainloop()
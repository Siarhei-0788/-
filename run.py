from ui import MainWindow
from db import init_db

if __name__ == "__main__":
    init_db()
    app = MainWindow()
    app.mainloop()

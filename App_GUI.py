import tkinter as tk

import customtkinter as ctk

from sql_interface import DbChinook
from logic import Search_engine

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class Window(ctk.CTk):

    WIDTH = 1248
    HEIGHT = 732
    
    LARGE_FONT = ("Comic Sans MS", 24)
    MEDIUM_FONT = ("Comic Sans MS", 16)
    SMALL_FONT = ("Comic Sans MS", 12)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = DbChinook()
        self.search_engine = Search_engine(self.db)

        self.WINDOW_CENTERING_X = int(self.winfo_screenwidth()/2 - self.WIDTH/2)
        self.WINDOW_CENTERING_Y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)

        self.title("Track Finder App")
        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{self.WINDOW_CENTERING_X}+{self.WINDOW_CENTERING_Y}"
        )
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Call .on_closing() when app gets closed

        self.create_widgets()

    def create_widgets(self):
        """Fills the window with widgets
        """
        # Left frame
        self.frame_left = ctk.CTkFrame(self, width=180, height=832, corner_radius=0)
        self.frame_left.grid(row=0, column=0, rowspan=12, sticky="nswe")
        
        self.frame_left.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 11), minsize=10)
        
        self.label_1 = ctk.CTkLabel(self.frame_left, text="Track\nFinder\nApp",
                                    text_font=self.LARGE_FONT)
        self.label_1.grid(row=0, column=0, pady=20, padx=10)
        
        self.label_mode = ctk.CTkLabel(self.frame_left, text="Appearance Mode:", 
                                       text_font=self.SMALL_FONT
        )
        self.label_mode.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.appearance_mode = ctk.CTkOptionMenu(self.frame_left,
                                              values=["Light", "Dark"],
                                              command=self.change_appearance_mode)
        self.appearance_mode.set("Dark")
        self.appearance_mode.grid(row=10, column=0, pady=(0, 20), padx=20, sticky="w")
        # ------------------------
        
        ctk.CTkLabel(self, text="Введіть пошуковий запит:", 
                     text_font=self.MEDIUM_FONT
        ).grid(row=0, column=1, columnspan=3, rowspan=2, 
               sticky="w", padx=20, pady=20
        )
        
        self.entry = ctk.CTkEntry(self, width=440, placeholder_text="Сюди", 
                                  text_font=self.MEDIUM_FONT
        )
        self.entry.grid(row=2, column=1, columnspan=3, rowspan=2, 
                        pady=(0, 20), padx=20, sticky="we"
        )
        
        # Frame with listbox and scrollbars
        self.frame_listbox = ctk.CTkFrame(self, width=440, height=500)
        self.frame_listbox.grid(row=4, column=1, columnspan=3, 
                                rowspan=8, pady=(0, 20), padx=20, sticky="nswe"
        )
        
        self.listbox = tk.Listbox(self.frame_listbox, bg="#1f1f1f",
                                  selectbackground="light gray", 
                                  selectmode="single", bd=2, 
                                  highlightthickness=0, 
                                  font=self.MEDIUM_FONT, 
                                  relief="groove", height=19, width=36
        )
        self.listbox.grid(row=0, column=0, sticky="nswe")
        
        self.listbox_scroll_y = ctk.CTkScrollbar(self.frame_listbox, 
                                                 command=self.listbox.yview
        )
        self.listbox_scroll_y.grid(row=0, column=1, sticky="ns")
        
        self.listbox_scroll_x = ctk.CTkScrollbar(self.frame_listbox, height=17, 
                                                 command=self.listbox.xview
        )
        self.listbox_scroll_x.grid(row=1, column=0, columnspan=2, sticky="we")

        self.listbox.configure(yscrollcommand=self.listbox_scroll_y.set, 
                               xscrollcommand=self.listbox_scroll_x.set
        )

    def search_track(self):
        """Пошук треків за назвою треку, або за автором
        або за жанром, в залежності від обраного режиму
        radiobutton
        """
        pass

    def click_track(self):
        """Добуває детальну інформацію про обраний
        трек
        """
        pass

    def change_appearance_mode(self, new_appearance_mode):
        if new_appearance_mode == "Dark":
            self.listbox["bg"] = "#1f1f1f"
            self.listbox["fg"] = "#ebebeb"
        elif new_appearance_mode == "Light":
            self.listbox["bg"] = "#ebebeb"
            self.listbox["fg"] = "#1f1f1f"
        ctk.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    root = Window()
    root.mainloop()
import tkinter as tk

import customtkinter as ctk

from sql_interface import DbChinook
from logic import Search_engine

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class Window(ctk.CTk):

    WIDTH = 1248
    HEIGHT = 720
    
    LARGE_FONT = ("Comic Sans MS", 24)
    MEDIUM_FONT = ("Comic Sans MS", 16)
    SMALL_FONT = ("Comic Sans MS", 12)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resizable(False, False)

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
        
        self.label_1 = ctk.CTkLabel(self.frame_left, text="Track\nFinder\nApp",
                                    text_font=self.LARGE_FONT)
        self.label_1.pack(pady=60, padx=10)
        
        self.appearance_mode = ctk.CTkOptionMenu(self.frame_left, 
                                              values=["Light", "Dark"],
                                              command=self.change_appearance_mode)
        self.appearance_mode.set("Dark")
        self.appearance_mode.pack(pady=(0, 80), padx=20, side="bottom")
        
        self.label_mode = ctk.CTkLabel(self.frame_left, text="Appearance Mode:", 
                                       text_font=self.SMALL_FONT
        )
        self.label_mode.pack(pady=20, padx=20, side="bottom")
        # ------------------------
        
        ctk.CTkLabel(self, text="Введіть пошуковий запит:", 
                     text_font=self.MEDIUM_FONT
        ).grid(row=0, column=1, columnspan=3, rowspan=2, 
               sticky="w", padx=20, pady=20
        )
        
        self.entry = ctk.CTkEntry(self, width=440, placeholder_text="Сюди", 
                                  text_font=self.MEDIUM_FONT
        )
        self.entry.grid(row=1, column=1, columnspan=3, rowspan=3, 
                        pady=(0, 20), padx=20, sticky="we"
        )
        
        # Frame with listbox and scrollbars
        self.frame_listbox = ctk.CTkFrame(self, width=440, height=500, corner_radius=0)
        self.frame_listbox.grid(row=4, column=1, columnspan=3, 
                                rowspan=8, pady=(0, 20), padx=20, sticky="nswe"
        )
        
        self.listbox = tk.Listbox(self.frame_listbox, bg="#1f1f1f",
                                  selectbackground="light gray", 
                                  selectmode="single", bd=2, 
                                  highlightthickness=0, 
                                  font=self.MEDIUM_FONT, 
                                  relief="groove", height=16, width=36
        )
        self.listbox.grid(row=0, column=0, sticky="nswe")
        
        self.listbox_scroll_y = ctk.CTkScrollbar(self.frame_listbox, 
                                                 command=self.listbox.yview
        )
        self.listbox_scroll_y.grid(row=0, column=1, sticky="ns")
        
        self.listbox_scroll_x = ctk.CTkScrollbar(self.frame_listbox, height=16, 
                                                 command=self.listbox.xview
        )
        self.listbox_scroll_x.grid(row=1, column=0, sticky="we")

        self.listbox.configure(yscrollcommand=self.listbox_scroll_y.set, 
                               xscrollcommand=self.listbox_scroll_x.set
        )
        # ------------------------

        self.search_button = ctk.CTkButton(self, text="Search", 
                                           text_font=self.MEDIUM_FONT,
                                           command=self.search_track
        )
        self.search_button.grid(row=1, column=4, rowspan=3, 
                                pady=(0, 20), padx=20, sticky="we"
        )

        # Radiobuttons
        self.radio_var = tk.IntVar(value=0)

        self.label_radio_group = ctk.CTkLabel(self, text="Шукати...", text_font=self.SMALL_FONT)
        self.label_radio_group.grid(row=0, column=6, pady=20, padx=(40, 20), sticky="w")

        self.radio_button_1 = ctk.CTkRadioButton(self, variable=self.radio_var,
                                                 value=0, text="За назвою", text_font=self.SMALL_FONT
        )
        self.radio_button_1.grid(row=1, column=6, pady=(0, 20), padx=(40, 20), sticky="w")

        self.radio_button_2 = ctk.CTkRadioButton(self, variable=self.radio_var,
                                                 value=1, text="За автором", text_font=self.SMALL_FONT
        )
        self.radio_button_2.grid(row=2, column=6, pady=(0, 20), padx=(40, 20), sticky="w")

        self.radio_button_3 = ctk.CTkRadioButton(self, variable=self.radio_var,
                                                 value=2, text="За жанром", text_font=self.SMALL_FONT
        )
        self.radio_button_3.grid(row=3, column=6, pady=(0, 20), padx=(40, 20), sticky="w")
        # ------------------------

        # Frame with labels
        self.frame_labels = ctk.CTkFrame(self, width=480, height=480)
        self.frame_labels.grid(row=4, column=4, columnspan=3, 
                               rowspan=8, pady=(0, 20), padx=20, sticky="nswe"
        )
        self.frame_labels.pack_propagate(0)

        self.name = tk.StringVar(value="Назва обраної пісні")
        self.label_2 = ctk.CTkLabel(self.frame_labels, textvariable=self.name, 
                                    text_font=self.LARGE_FONT, anchor="center")
        self.label_2.pack(padx=10, pady=20)

        self.author = tk.StringVar(value="Автор")
        self.label_3 = ctk.CTkLabel(self.frame_labels, textvariable=self.author, 
                                    text_font=self.LARGE_FONT, anchor="center", 
                                    corner_radius=17, width=400, fg_color=("white", "gray55"), 
                                    height=70)
        self.label_3.pack(padx=10, pady=(40, 0))

        self.name_album = tk.StringVar(value="Назва альбому")
        self.label_4 = ctk.CTkLabel(self.frame_labels, textvariable=self.name_album, 
                                    text_font=self.LARGE_FONT, anchor="center", 
                                    corner_radius=17, width=400, fg_color=("white", "gray55"), 
                                    height=70)
        self.label_4.pack(padx=10, pady=(40, 0))

        self.duration = tk.StringVar(value="Тривалість")
        self.label_5 = ctk.CTkLabel(self.frame_labels, textvariable=self.duration, 
                                    text_font=self.LARGE_FONT, anchor="center", 
                                    width=400, fg_color=("white", "gray55"), 
                                    corner_radius=17, height=70)
        self.label_5.pack(padx=10, pady=(40, 0))

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
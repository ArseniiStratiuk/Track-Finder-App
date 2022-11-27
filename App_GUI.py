import tkinter as tk
import tkinter.font as tkFont
import os
import sys

import customtkinter as ctk
from PIL import Image, ImageTk

from sql_interface import DbChinook
from logic import Search_engine

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class Window(ctk.CTk):

    WIDTH = 1242
    HEIGHT = 720
    
    LARGE_FONT = ("Calibri", 24, "bold")
    MEDIUM_FONT = ("Calibri", 18, "bold")
    SMALL_FONT = ("Calibri", 14, "bold")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resizable(False, False)

        self.db = DbChinook()
        self.engine = Search_engine(self.db)

        self.WINDOW_CENTERING_X = int(self.winfo_screenwidth()/2 - self.WIDTH/2)
        self.WINDOW_CENTERING_Y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        
        self.SEARCH_DARK = ImageTk.PhotoImage(Image.open(
            os.path.join(sys.path[0], "Search_Image_Dark.png")
        ).resize((55, 55)))
        
        self.SEARCH_LIGHT = ImageTk.PhotoImage(Image.open(
            os.path.join(sys.path[0], "Search_Image_Light.png")
        ).resize((55, 55)))

        self.min = "хв"  # This changes according 
        self.sec = "с"   # to the chosen language.
        
        self.title("Додаток Пошуку Треків")
        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{self.WINDOW_CENTERING_X}+{self.WINDOW_CENTERING_Y}"
        )
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Call .on_closing() when app gets closed
        
        self.create_widgets()
        
        self.fill_listbox_with_tracks()
        
        self.listbox.bind("<<ListboxSelect>>", self.click_track)

    def create_widgets(self):
        """Fills the window with widgets
        """
        # Left frame
        self.frame_left = ctk.CTkFrame(self, width=180, height=832, corner_radius=0)
        self.frame_left.grid(row=0, column=0, rowspan=12, sticky="nswe")
        
        self.label_1 = ctk.CTkLabel(self.frame_left, text="Додаток\nПошуку\nТреків", 
                                    text_font=self.LARGE_FONT)
        self.label_1.pack(pady=60, padx=10)
        
        self.appearance_mode = ctk.CTkOptionMenu(self.frame_left, text_font="Calibri 12", 
                                              values=["Світлий", "Темний"], 
                                              command=self.change_appearance_mode)
        self.appearance_mode.set("Темний")
        self.appearance_mode.pack(pady=(0, 80), padx=20, side="bottom")
        
        self.label_mode = ctk.CTkLabel(self.frame_left, text="Вигляд вікна:", 
                                       text_font=self.SMALL_FONT)
        self.label_mode.pack(pady=20, padx=20, side="bottom")
        # ------------------------
        
        ctk.CTkLabel(self, text="Введіть пошуковий запит:", 
                     text_font=self.MEDIUM_FONT).grid(row=0, column=1, 
                                                      columnspan=3, rowspan=2, 
                                                      sticky="w", padx=20, pady=20)
        
        self.search_query = tk.StringVar()
        self.search_query.trace_add("write", self.fill_listbox_with_tracks)
        self.entry = ctk.CTkEntry(self, width=440, placeholder_text="Сюди", 
                                  text_font=self.MEDIUM_FONT, height=45, 
                                  textvariable=self.search_query, corner_radius=10, 
                                  selectbackground="#11b384")
        self.entry.grid(row=1, column=1, columnspan=3, rowspan=3, 
                        pady=(0, 20), padx=20, sticky="we")
        
        # Frame with listbox and scrollbars
        self.frame_listbox = ctk.CTkFrame(self, width=440, height=500, corner_radius=0)
        self.frame_listbox.grid(row=4, column=1, columnspan=3, 
                                rowspan=8, pady=(0, 20), padx=20, sticky="nswe")
        
        self.listbox = tk.Listbox(self.frame_listbox, bg="#1f1f1f", fg="#ebebeb", 
                                  selectbackground="#11b384", cursor="hand2", 
                                  selectmode="browse", bd=2, activestyle="none", 
                                  highlightthickness=0, selectforeground="#ebebeb", 
                                  font=self.MEDIUM_FONT, exportselection=False, 
                                  relief="groove", height=16, width=40)
        self.listbox.grid(row=0, column=0, sticky="nswe")
        
        self.listbox_scroll_y = ctk.CTkScrollbar(self.frame_listbox, 
                                                 command=self.listbox.yview)
        self.listbox_scroll_y.grid(row=0, column=1, sticky="ns")
        
        self.listbox_scroll_x = ctk.CTkScrollbar(self.frame_listbox, 
                                                 command=self.listbox.xview, 
                                                 orientation="horizontal")
        self.listbox_scroll_x.grid(row=1, column=0, sticky="we")

        self.listbox.configure(yscrollcommand=self.listbox_scroll_y.set, 
                               xscrollcommand=self.listbox_scroll_x.set)
        # ------------------------

        self.search_button = ctk.CTkButton(self, text="Пошук", image=self.SEARCH_LIGHT, 
                                           text_font=self.MEDIUM_FONT, compound="left", 
                                           command=self.fill_listbox_with_tracks, 
                                           width=75, height=70, corner_radius=10)
        self.search_button.grid(row=1, column=4, rowspan=3, 
                                pady=(0, 20), padx=20)

        # Radiobuttons
        self.search_mode = tk.StringVar(value="name")
        self.search_mode.trace_add("write", self.fill_listbox_with_tracks)

        self.label_radio_group = ctk.CTkLabel(self, text="Шукати...", 
                                              text_font=self.SMALL_FONT)
        self.label_radio_group.grid(row=0, column=6, pady=20, 
                                    padx=(40, 20), sticky="w")

        self.radio_button_name = ctk.CTkRadioButton(self, variable=self.search_mode, 
                                                    value="name", text="За назвою", 
                                                    text_font=self.SMALL_FONT)
        self.radio_button_name.grid(row=1, column=6, pady=(0, 20), 
                                    padx=(40, 20), sticky="w")

        self.radio_button_author = ctk.CTkRadioButton(self, variable=self.search_mode,
                                                      value="author", text="За автором", 
                                                      text_font=self.SMALL_FONT)
        self.radio_button_author.grid(row=2, column=6, pady=(0, 20), 
                                      padx=(40, 20), sticky="w")

        self.radio_button_genre = ctk.CTkRadioButton(self, variable=self.search_mode,
                                                     value="genre", text="За жанром", 
                                                     text_font=self.SMALL_FONT)
        self.radio_button_genre.grid(row=3, column=6, pady=(0, 20), 
                                     padx=(40, 20), sticky="w")
        # ------------------------

        # Frame with labels
        self.frame_labels = ctk.CTkFrame(self, width=480, height=480)
        self.frame_labels.grid(row=4, column=4, columnspan=3, 
                               rowspan=8, pady=(0, 20), padx=20, sticky="nswe")
        self.frame_labels.pack_propagate(0)

        self.name = tk.StringVar(value="Назва обраної пісні")
        self.label_name = ctk.CTkLabel(self.frame_labels, textvariable=self.name, 
                                       text_font=self.LARGE_FONT, anchor="center", 
                                       width=400)
        self.label_name.pack(padx=10, pady=20)

        self.author = tk.StringVar(value="Автор")
        self.label_author = ctk.CTkLabel(self.frame_labels, textvariable=self.author, 
                                        text_font=self.MEDIUM_FONT, anchor="center", 
                                        corner_radius=10, width=400, 
                                        fg_color=("gray97", "gray28"), height=50)
        self.label_author.pack(padx=10, pady=(40, 0))

        self.genre = tk.StringVar(value="Жанр пісні")
        self.label_genre = ctk.CTkLabel(self.frame_labels, textvariable=self.genre, 
                                        text_font=self.MEDIUM_FONT, anchor="center", 
                                        corner_radius=10, width=400, 
                                        fg_color=("gray97", "gray28"), height=50)
        self.label_genre.pack(padx=10, pady=(40, 0))

        self.album = tk.StringVar(value="Назва альбому")
        self.label_album = ctk.CTkLabel(self.frame_labels, textvariable=self.album, 
                                       text_font=self.MEDIUM_FONT, anchor="center", 
                                       width=400, fg_color=("gray97", "gray28"), 
                                       corner_radius=10, height=50)
        self.label_album.pack(padx=10, pady=(40, 0))

        self.duration = tk.StringVar(value="Тривалість")
        self.label_duration = ctk.CTkLabel(self.frame_labels, textvariable=self.duration, 
                                           text_font=self.MEDIUM_FONT, anchor="center", 
                                           width=400, fg_color=("gray97", "gray28"), 
                                           corner_radius=10, height=50)
        self.label_duration.pack(padx=10, pady=(40, 0))

    def search_tracks(self, text) -> list:
        """
        Search for tracks either by their name or author(s) 
        or genre, depending on the selected mode (radiobutton).
        """
        if self.search_mode.get() == "name":
            tracks = self.engine.search_by_name(text)
            
        elif self.search_mode.get() == "author":
            tracks = self.engine.search_by_author(text)
            
        elif self.search_mode.get() == "genre":
            tracks = self.engine.search_by_genre(text)
        
        return tracks

    def click_track(self, event):
        """
        Fill labels with information 
        about the selected (clicked) track.
        """
        try:
            index = int(self.listbox.curselection()[0])
        except IndexError:
            return
        
        track = self.listbox.get(index)
        self.fit_text_in_name_label(track)
        
        data = self.engine.select_data(track)
        
        author = data[0]
        self.fit_text_in_author_label(author)
        
        genre = data[1]
        self.genre.set(genre)
        
        album = data[2]
        self.fit_text_in_album_label(album)
        
        duration = data[3]
        self.duration.set(self.milliseconds(duration))

    def change_appearance_mode(self, new_appearance_mode):
        """
        Change the window's theme (Dark or Light).
        """
        if new_appearance_mode == "Темний":
            self.listbox["bg"] = "#1f1f1f"
            self.listbox["fg"] = "#ebebeb"
            self.listbox["selectbackground"] = "#11b384"
            self.listbox["selectforeground"] = "#ebebeb"
            self.search_button.configure(image=self.SEARCH_LIGHT)
            self.entry["selectbackground"] = "#11b384"
            self.entry["selectforeground"] = "#ebebeb"
            ctk.set_appearance_mode("Dark")
        elif new_appearance_mode == "Світлий":
            self.listbox["bg"] = "#ebebeb"
            self.listbox["fg"] = "#1f1f1f"
            self.listbox["selectbackground"] = "#72cf9f"
            self.listbox["selectforeground"] = "#1f1f1f"
            self.search_button.configure(image=self.SEARCH_DARK)
            self.entry["selectbackground"] = "#72cf9f"
            self.entry["selectforeground"] = "#1f1f1f"
            ctk.set_appearance_mode("Light")
            
    def fill_listbox_with_tracks(self, *args):
        """
        Fill listbox with tracks that match the user's search query.
        """
        self.listbox.delete(0, "end")
        for i in self.search_tracks(self.search_query.get()):
            self.listbox.insert("end", i[0])
        if len(self.search_tracks(self.search_query.get())) == 0:
            self.name.set("Жодного треку не обрано")
            self.author.set("Автор")
            self.genre.set("Жанр пісні")
            self.album.set("Назва альбому")
            self.duration.set("Тривалість")
            
    def fit_text_in_name_label(self, text):
        """
        Fit overlong text in the label which 
        contains track's name by changing its last 
        characters with three dots.
        """
        
        font = tkFont.Font(family="Calibri", size=24, weight="bold")
        max_width = self.label_name.winfo_width()
        actual_width = font.measure(text)
        
        if actual_width <= max_width:
            # The original text fits; no need to add ellipsis.
            self.name.set(text)
        else:
            # The original text won't fit. Keep shrinking until it does.
            while actual_width > max_width and len(text) > 1:
                text = text[:-1]
                actual_width = font.measure(text + "...")
            self.name.set(text + "...")
            
    def fit_text_in_author_label(self, text):
        """
        Fit overlong text in the label which 
        contains track's author(s) by changing its last 
        characters with three dots.
        """
        
        font = tkFont.Font(family='Calibri', size=18, weight="bold")
        max_width = 376
        actual_width = font.measure(text)
        
        if actual_width <= max_width:
            # The original text fits; no need to add ellipsis.
            self.author.set(text)
        else:
            # The original text won't fit. Keep shrinking until it does.
            while actual_width > max_width and len(text) > 1:
                text = text[:-1]
                actual_width = font.measure(text + "...")
            self.author.set(text + "...")
            
    def fit_text_in_album_label(self, text):
        """
        Fit overlong text in the label which 
        contains track's album title by changing its last 
        characters with three dots.
        """
        
        font = tkFont.Font(family="Calibri", size=18, weight="bold")
        max_width = 376
        actual_width = font.measure(text)
        
        if actual_width <= max_width:
            # The original text fits; no need to add ellipsis.
            self.album.set(text)
        else:
            # The original text won't fit. Keep shrinking until it does.
            while actual_width > max_width and len(text) > 1:
                text = text[:-1]
                actual_width = font.measure(text + "...")
            self.album.set(text + "...")

    def milliseconds(self, number) -> str:
        """
        Convert milliseconds to seconds and minutes.
        """
        milliseconds = int(number)
        seconds = str(int((milliseconds/1000) % 60))
        minutes = str(int((milliseconds / (1000*60)) % 60))
        return f"{minutes} {self.min} {seconds} {self.sec}"

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    root = Window()
    root.mainloop()
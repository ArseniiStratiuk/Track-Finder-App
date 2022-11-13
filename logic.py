# -*- coding: utf-8 -*-
from sql_interface import DbChinook


class Search_engine():
    def __init__(self, db):
        self.db = db

    def select_all_tracks(self):
        """Вибрати всі записи про треки та вивести їх
        """
        res = self.db.select("""
                SELECT * FROM tracks;
        """)
        print(res)
        
    def search_track(self, search_text):
        search_text = f"%{search_text}%"


if __name__ == '__main__':   
   db = DbChinook()
   engine = Search_engine(db)
   engine.select_all_tracks()
# -*- coding: utf-8 -*-


class Search_engine():
    def __init__(self, db):
        self.db = db

    def select_all_tracks(self):
        """
        Вибрати всі записи про треки та вивести їх
        """
        res = self.db.select("""
                SELECT * FROM tracks;
        """)
        print(res)


if __name__ == '__main__':
   from sql_interface import DbChinook
   
   db = DbChinook()
   engine = Search_engine(db)
   engine.select_all_tracks()
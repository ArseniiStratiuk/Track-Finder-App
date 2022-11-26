# -*- coding: utf-8 -*-
from sql_interface import DbChinook


class Search_engine():
    def __init__(self, db):
        self.db = db
    
    def select_data(self, track):
        """
        Select information about the chosen track: author(s) 
        or artist(s), its genre, name of the album and its duration 
        in milliseconds.
        """
        res = self.db.select("""
                SELECT ar.Name, g.Name, al.Title, t.Milliseconds 
                FROM tracks t INNER JOIN genres g USING (GenreId) 
                INNER JOIN albums al USING (AlbumId) 
                INNER JOIN artists ar USING (ArtistId) 
                WHERE t.Name = ?;
        """, track)
        return res[0]
        
    def search_by_name(self, search_text):
        search_text = f"%{search_text}%"
        res = self.db.select("""
                SELECT Name FROM tracks WHERE Name LIKE ?;
        """, search_text)
        return res
        
    def search_by_author(self, search_text):
        search_text = f"%{search_text}%"
        res = self.db.select("""
                SELECT t.Name FROM tracks t 
                INNER JOIN albums USING (AlbumId) 
                INNER JOIN artists ar USING (ArtistId) 
                WHERE ar.Name LIKE ?;
        """, search_text)
        return res
        
    def search_by_genre(self, search_text):
        search_text = f"%{search_text}%"
        res = self.db.select("""
                SELECT t.Name FROM tracks t 
                INNER JOIN genres g USING (GenreId) 
                WHERE g.Name LIKE ?;
        """, search_text)
        return res

if __name__ == '__main__':
   db = DbChinook()
   engine = Search_engine(db)
#    print(engine.search_by_name('fast'))
#    print(engine.search_by_author('ac/dc'))
#    print(engine.search_by_genre('pop'))
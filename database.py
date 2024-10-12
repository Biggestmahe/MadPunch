import sqlite3
import os
connection = sqlite3.connect("Project.db")
cursor = connection.cursor()

#trying to make an database(if is has not been made)
def make_database ():

    try :
        sqlcommand = """
            CREATE TABLE tblUserData
           (
            UserId INTEGER,
            Username TEXT,
            Password TEXT,
            Key TEXT,
            Number_of_played_games INTEGER,
            Won INTEGER,
            Lost INTEGER,
            Score INTEGER,
            Primary key (UserId)
            )"""

        cursor.execute(sqlcommand)
        connection.commit()
    
    except :
        pass




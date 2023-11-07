import sqlite3

connection = sqlite3.connect('my_first_data_base.sqlite')
cursor = connection.cursor()
# cursor.execute('DROP TABLE IF EXISTS AlbumsList')
# cursor.execute('''CREATE TABLE IF NOT EXISTS AlbumsList (
#                  album_name TEXT PRIMARY KEY NOT NULL
#                 )''')
connection.commit()
names_list = [row[0] for row in cursor.fetchall()]  # получаем список названий альбомов
cursor.execute('SELECT id FROM AlbumsList')

# max_id = max([int(row[1]) for row in cursor.fetchall()])
# print(cursor.fetchall(), names_list)
cursor.execute(f'''INSERT INTO AlbumsList (album_name) VALUES ('d')''')
connection.commit()
# print(max_id)

# # cursor.execute('''CREATE TABLE IF NOT EXISTS Album
# #                 (
# #                 id INTEGER PRIMARY KEY,
# #                 photo_path TEXT NOT NULL,
# #                 photo_id_album INTEGER NOT NULL
# #                 )
# #                ''')
# # connection.commit()
# cursor.execute('''CREATE TABLE IF NOT EXISTS AlbumsList
#                 (
#                 album_name TEXT NOT NULL AND PRIMARY KEY,
#                 album_name TEXT NOT NULL
#                 )
#                ''')
# connection.commit()
# a = ['a', 'b', 'c', 'd']
# for i in range(len(a)):
#     cursor.execute(f'''INSERT INTO AlbumsList (id, album_name) VALUES ({i}, '{a[i]}')''')
#
# connection.commit()
#

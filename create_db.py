import sqlite3
# Kết nối đến cơ sở dữ liệu SQLite (nếu chưa tồn tại, sẽ được tạo mới)
conn = sqlite3.connect("face.db")
# conn = sqlite3.connect("db/analytic.db")
cursor = conn.cursor()

# Tạo bảng states với datetime và entity_id không được lặp lại
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faces (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        encoding BLOB NOT NULL,
        image BLOB NOT NULL
    )
''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
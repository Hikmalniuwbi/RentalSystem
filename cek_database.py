import sqlite3
DB_NAME = "rental_app.db"

def inspect_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n" + "="*50)
        print("DATABASE INSPECTOR (SQLite)".center(50))
        print("="*50)

        if not tables:
            print("\nDatabase masih kosong (belum ada tabel).")
            return

        for table in tables:
            table_name = table[0]
            print(f"\n[ TABEL: {table_name.upper()} ]")
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print(" Kolom: " + " | ".join(columns))
            print("-" * 50)
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print("  (Tabel Kosong)")
            else:
                for row in rows:
                    print("  " + " | ".join(map(str, row)))
            print("-" * 50)
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_db()

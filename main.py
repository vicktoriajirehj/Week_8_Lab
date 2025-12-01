import sqlite3
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from import_and_constants import DB_PATH


def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    def migrate_users_from_file(conn, filepath = "C:/CST1510_LABS/users.txt"):
        """
            Migrate users from users.txt to the database.

            This is a COMPLETE IMPLEMENTATION as an example.

            Args:
                conn: Database connection
                filepath: Path to users.txt file
            """
        if not filepath.exists():
            print(f"⚠️  File not found: {filepath}")
            print("   No users to migrate.")
            return

        cursor = conn.cursor()
        migrated_count = 0

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Parse line: username,password_hash
                parts = line.split(',')
                if len(parts) >= 2:
                    username = parts[0]
                    password_hash = parts[1]

                    # Insert user (ignore if already exists)
                    try:
                        cursor.execute(
                            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                            (username, password_hash, 'user')
                        )
                        if cursor.rowcount > 0:
                            migrated_count += 1
                    except sqlite3.Error as e:
                        print(f"Error migrating user {username}: {e}")

        conn.commit()
        print(f"✅ Migrated {migrated_count} users from {filepath.name}")

    #verify that the migration of the users file was succesful
    # Verify users were migrated
    conn = connect_database()
    cursor = conn.cursor()

    # Query all users
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    print(" Users in database:")
    print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
    print("-" * 35)
    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

    print(f"\nTotal users: {len(users)}")
    conn.close()


    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 4. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")


if __name__ == "__main__":
    main()

  #connect to database
def connect_database(db_path = DB_PATH):
    return sqlite3.connect(str(db_path))


def migrate_users_from_file(conn, filepath= "C:/CST1510_LABS/users.txt" / "users.txt"):
    """
    Migrate users from users.txt to the database.

    This is a COMPLETE IMPLEMENTATION as an example.

    Args:
        conn: Database connection
        filepath: Path to users.txt file
    """
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return

    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")
# Verify users were migrated
conn = connect_database()
cursor = conn.cursor()

# Query all users
cursor.execute("SELECT id, username, role FROM users")
users = cursor.fetchall()

print(" Users in database:")
print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
print("-" * 35)
for user in users:
    print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

print(f"\nTotal users: {len(users)}")
conn.close()


def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "=" * 60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")

    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")

    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")

    conn.close()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


# Run tests
run_comprehensive_tests()
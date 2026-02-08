import bcrypt

print("Testing bcrypt functionality...")

try:
    # Test basic bcrypt functionality
    password = "testpassword123"
    print(f"Original password: {password}")

    # Encode to bytes
    password_bytes = password.encode('utf-8')
    print(f"Encoded to bytes: {len(password_bytes)} bytes")

    # Generate salt and hash
    salt = bcrypt.gensalt()
    print(f"Salt generated: {salt}")

    hashed = bcrypt.hashpw(password_bytes, salt)
    print(f"Password hashed: {hashed}")

    # Verify
    is_valid = bcrypt.checkpw(password_bytes, hashed)
    print(f"Password verification: {is_valid}")

    print("✅ Basic bcrypt functionality works!")

except Exception as e:
    print(f"❌ Bcrypt error: {e}")
    import traceback
    traceback.print_exc()
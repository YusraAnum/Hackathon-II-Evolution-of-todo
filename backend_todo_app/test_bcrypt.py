from passlib.context import CryptContext

print("Testing bcrypt functionality...")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    # Truncate password to 72 bytes to comply with bcrypt limitations
    truncated_password = password[:72] if len(password) > 72 else password
    print(f'Truncating password from {len(password)} to {len(truncated_password)} chars')
    return pwd_context.hash(truncated_password)

try:
    print("Attempting to hash password 'testpass'...")
    hashed = hash_password('testpass')
    print(f'Password hashed successfully: {hashed[:20]}...')
    
    # Test verification
    verified = pwd_context.verify('testpass', hashed)
    print(f'Password verification result: {verified}')
except Exception as e:
    print(f'Error hashing password: {e}')
    import traceback
    traceback.print_exc()
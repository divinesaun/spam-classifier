import secrets
import string

def generate_api_key(length=32):
    """Generates a secure API key."""
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for i in range(length))
    return api_key

if __name__ == "__main__":
    key = generate_api_key()
    print(f"Generated API Key: {key}")
    print("\nAdd this to your database 'api_keys' table or set as MASTER_API_KEY env var.")

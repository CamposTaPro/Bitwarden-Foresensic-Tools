import os
import plyvel
import re
import json
import platform

try:
    # Detect the operating system
    is_windows = platform.system().lower() == "windows"

    # Set the database path based on the OS
    if is_windows:
        userprofile = os.getenv("userprofile")  # For Windows
        db_path = os.path.join(userprofile, "AppData", "Local", "Google", "Chrome", "User Data", 
                               "Default", "Local Extension Settings", "nngceckbapebfimnlniiiahkandclblb")
    else:
        userprofile = os.getenv("HOME")  # For Linux/macOS
        db_path = os.path.join(userprofile, ".config", "google-chrome", "Default", 
                               "Local Extension Settings", "nngceckbapebfimnlniiiahkandclblb")

    # Open the LevelDB database
    try:
        db = plyvel.DB(db_path, create_if_missing=False)
    except Exception as e:
        raise FileNotFoundError(f"Unable to open LevelDB at {db_path}. Ensure the path is correct. Error: {e}")

    # Step 1: Extract the User ID
    try:
        # Retrieve the active account ID from the database
        user_id_raw = db.get(b'global_account_activeAccountId').decode()
        # Split the raw data to isolate the user ID
        user_id_parts = user_id_raw.split("\"")
        flattened_string = ' '.join(user_id_parts)

        # Use a regular expression to extract the UUID format UserID
        user_id_match = re.search(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', flattened_string)
        if not user_id_match:
            raise ValueError("UserID not found in the database.")
        user_id = str(user_id_match.group(0))
        print("UserID:", user_id)
    except Exception as e:
        raise RuntimeError(f"Failed to extract UserID. Error: {e}")

    # Step 2: Extract kdfType and Iterations
    try:
        # Construct the query to retrieve the KDF configuration
        kdf_query = f'user_{user_id}_kdfConfig_kdfConfig'.encode()
        kdf_config_raw = db.get(kdf_query).decode()

        # Parse the KDF configuration JSON
        kdf_config_json = json.loads(kdf_config_raw)
        nested_kdf_config = json.loads(kdf_config_json['value'])

        # Extract KDF type and iterations
        kdf_type = nested_kdf_config['kdfType']
        iterations = nested_kdf_config['iterations']
        print("KDF Type:", kdf_type)
        print("Iterations:", iterations)
    except Exception as e:
        raise RuntimeError(f"Failed to extract KDF Type and Iterations. Error: {e}")

    # Step 3: Extract the user's email
    try:
        # Retrieve the account information from the database
        accounts_raw = db.get(b'global_account_accounts').decode()
        accounts_json = json.loads(accounts_raw)
        nested_accounts = json.loads(accounts_json['value'])

        # Extract the email address associated with the user ID
        email = nested_accounts[user_id]['email']
        print("Email:", email)
    except Exception as e:
        raise RuntimeError(f"Failed to extract email. Error: {e}")

    # Step 4: Extract the Master Key Hash
    try:
        # Construct the query to retrieve the Master Key Hash
        master_key_query = f'user_{user_id}_masterPassword_masterKeyHash'.encode()
        master_key_raw = db.get(master_key_query).decode()

        # Parse the Master Key Hash JSON
        master_key_json = json.loads(master_key_raw)

        # Extract and clean up the Master Key Hash value
        master_key_hash = master_key_json['value'].replace('"', '')
        print("Master Key Hash:", master_key_hash)
    except Exception as e:
        raise RuntimeError(f"Failed to extract Master Key Hash. Error: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the database is closed properly
    try:
        db.close()
    except Exception:
        pass

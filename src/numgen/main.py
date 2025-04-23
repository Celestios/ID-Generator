import hashlib
import hmac
import json
import os
import secrets
import random
import string


class AnonymousIDGenerator:
    def __init__(self, storage_file="anonymous_ids.json", key_file="secret.key", salt_length=16, id_length=10):
        self.storage_file = storage_file
        self.key_file = key_file
        self.salt_length = salt_length
        self.id_length = id_length
        self.char_set = string.ascii_letters + string.digits + "!@#$%^&*"
        self.secret_key = self._load_or_generate_key()
        self.id_map = self._load_mapping()

    def _load_or_generate_key(self):
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, "rb") as f:
                    return f.read()
            else:
                key = secrets.token_bytes(32)  # 256-bit key
                with open(self.key_file, "wb") as f:
                    f.write(key)
                return key
        except (IOError, OSError) as e:
            raise RuntimeError(f"Failed to load or create key file: {e}")

    def _secure_key_from_real_id(self, real_id: str) -> str:
        return hmac.new(self.secret_key, real_id.encode(), hashlib.sha256).hexdigest()

    def _load_mapping(self):
        if not os.path.exists(self.storage_file):
            return {}
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load ID map ({e}), starting fresh.")
            return {}

    def _save_mapping(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.id_map, f)
        except (IOError, OSError) as e:
            raise RuntimeError(f"Failed to save ID map: {e}")

    def generate_anonymous_id(self, real_id: int) -> str:
        real_id_str = str(real_id)
        key = self._secure_key_from_real_id(real_id_str)

        if key in self.id_map:
            salt = self.id_map[key]['salt']
            anon_id = self._generate_short_id(real_id_str, salt)
            if anon_id != self.id_map[key]['anonymous_id']:
                salt = secrets.token_hex(self.salt_length)
                anon_id = self._generate_short_id(real_id_str, salt)
                self.id_map[key] = {'salt': salt, 'anonymous_id': anon_id}
                self._save_mapping()
            return anon_id
        else:
            salt = secrets.token_hex(self.salt_length)
            anon_id = self._generate_short_id(real_id_str, salt)
            self.id_map[key] = {'salt': salt, 'anonymous_id': anon_id}
            self._save_mapping()
            return anon_id

    def get_anonymous_id(self, real_id: int) -> str:
        real_id_str = str(real_id)
        key = self._secure_key_from_real_id(real_id_str)
        if key in self.id_map:
            return self.id_map[key]['anonymous_id']
        else:
            return self.generate_anonymous_id(real_id)

    def _generate_short_id(self, data: str, salt: str) -> str:
        salted_data = salt.encode('utf-8') + data.encode('utf-8')
        hash_digest = hashlib.sha256(salted_data).hexdigest()
        seed = int(hash_digest[:16], 16)
        rng = random.Random(seed)
        return ''.join(rng.choices(self.char_set, k=self.id_length))


# === Example Usage ===
if __name__ == "__main__":
    try:
        generator = AnonymousIDGenerator()

        real_id_1 = 12345
        anon_1 = generator.get_anonymous_id(real_id_1)
        print(f"Real ID: {real_id_1} → Anon ID: {anon_1}")

        anon_1_repeat = generator.get_anonymous_id(real_id_1)
        print(f"Real ID: {real_id_1} → Anon ID (again): {anon_1_repeat}")
        assert anon_1 == anon_1_repeat

        real_id_2 = 67890
        anon_2 = generator.get_anonymous_id(real_id_2)
        print(f"Real ID: {real_id_2} → Anon ID: {anon_2}")
    except Exception as e:
        print(f"Error: {e}")

import hashlib


def get_hash(key):
    """
    Return uppercase hash for given value
    Return it untouched if this value already a hash
    Converts key to lowercase before hashing
    """
    if not key:
        return False
    if is_hash(key):
        return key.upper()
    return hashlib.md5(key.lower().encode("utf-8")).hexdigest().upper()


def is_hash(value):
    return "::" not in value and len(value) == 32

from auth.security import hash_password, verify_password


def test_password_hash_and_verify_round_trip_uses_supported_scheme():
    password = "SecretPass123!"
    password_hash = hash_password(password)

    assert password_hash.startswith("$pbkdf2-sha256$")
    assert verify_password(password, password_hash) is True
    assert verify_password("wrong-password", password_hash) is False

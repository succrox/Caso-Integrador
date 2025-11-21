"""Tests para la clase Client.

Usamos pytest para validar creación, validación y serialización.
"""
import pytest
from datetime import datetime

from client import Client


def test_create_client_valid():
    c = Client(id=1, name="Ana Pérez", email="ana.perez@example.com")
    assert c.id == 1
    assert c.name == "Ana Pérez"
    assert c.email == "ana.perez@example.com"
    assert isinstance(c.created_at, datetime)


def test_invalid_email_raises():
    with pytest.raises(ValueError):
        Client(id=2, name="Bad", email="not-an-email")


def test_update_email_valid_and_invalid():
    c = Client(id=3, name="Bob", email="bob@example.com")
    c.update_email("bob.new@example.org")
    assert c.email == "bob.new@example.org"

    with pytest.raises(ValueError):
        c.update_email("invalid-email")


def test_to_from_dict_roundtrip():
    c = Client(id=4, name="Carmen", email="carmen@example.com", phone="+341234")
    d = c.to_dict()
    c2 = Client.from_dict(d)
    assert c2.id == c.id
    assert c2.name == c.name
    assert c2.email == c.email
    assert c2.phone == c.phone


def test_full_contact_and_phone_update():
    c = Client(id=5, name="Diego", email="diego@example.com")
    s = c.full_contact()
    assert "Diego" in s and "diego@example.com" in s and "N/A" in s

    c.update_phone("+34111222")
    s2 = c.full_contact()
    assert "+34111222" in s2

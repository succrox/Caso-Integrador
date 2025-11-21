"""Módulo con la clase Client.

Contiene una clase dataclass ligera para representar clientes, con
validación básica de email, serialización a/desde dict y métodos
de utilidad.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import re


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Client:
    """Representa un cliente.

    Attributes
    ----------
    id: int
        Identificador único del cliente.
    name: str
        Nombre completo del cliente.
    email: str
        Email del cliente (se valida al crear/actualizar).
    phone: Optional[str]
        Número de teléfono (opcional).
    address: Optional[str]
        Dirección postal o descriptiva (opcional).
    created_at: datetime
        Timestamp de creación; por defecto es el ahora UTC.

    Methods
    -------
    full_contact()
        Devuelve una cadena de contacto combinada (name <email> | phone).
    update_email(new_email)
        Valida y actualiza el email del cliente.
    update_phone(new_phone)
        Actualiza el teléfono.
    to_dict()
        Serializa el cliente a un dict (created_at en ISO format).
    from_dict(d)
        Crea una instancia a partir de un dict.
    validate_email(email)
        Valida el formato de email (método estático).
    """

    id: int
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        """Validación inicial tras la creación del dataclass.

        Lanza ValueError si el email no es válido.
        """
        if not self.validate_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")

    def full_contact(self) -> str:
        """Devuelve una cadena combinada con nombre, email y teléfono.

        Ejemplo: "Juan Pérez <juan@example.com> | +34123456789"
        """
        phone = self.phone if self.phone else "N/A"
        return f"{self.name} <{self.email}> | {phone}"

    def update_email(self, new_email: str) -> None:
        """Valida y actualiza el email del cliente.

        Parameters
        ----------
        new_email : str
            Nuevo email a asignar. Si no pasa la validación, se lanza ValueError.
        """
        if not self.validate_email(new_email):
            raise ValueError(f"Invalid email: {new_email}")
        self.email = new_email

    def update_phone(self, new_phone: Optional[str]) -> None:
        """Actualiza (o borra si se pasa None) el teléfono del cliente."""
        self.phone = new_phone

    def to_dict(self) -> Dict[str, Any]:
        """Serializa la instancia a un diccionario simple.

        La fecha `created_at` se convierte a ISO 8601 en UTC.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Client":
        """Crea una instancia de Client a partir de un diccionario.

        Si `created_at` es una cadena ISO, se parsea; si falta, se usa now.
        """
        created = d.get("created_at")
        if isinstance(created, str):
            try:
                created_dt = datetime.fromisoformat(created)
            except Exception:
                created_dt = datetime.utcnow()
        else:
            created_dt = datetime.utcnow()

        return cls(
            id=int(d["id"]),
            name=str(d["name"]),
            email=str(d["email"]),
            phone=d.get("phone"),
            address=d.get("address"),
            created_at=created_dt,
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida de forma sencilla si una cadena tiene formato de email.

        No pretende sustituir validaciones exhaustivas, pero evita errores
        obvios (sin @, sin dominio, espacios, etc.).
        """
        if not isinstance(email, str):
            return False
        return bool(EMAIL_RE.match(email.strip()))

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Client(id={self.id}, name={self.name})"

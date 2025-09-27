from __future__ import annotations

import random
import string
from dataclasses import dataclass
from datetime import datetime

from .settings import load_settings


@dataclass
class UserProfile:
    username: str
    password: str
    first_name: str
    last_name: str
    postal_code: str


def seed_random() -> None:
    seed = load_settings().app.seed
    random.seed(seed)


def random_username(prefix: str = "user") -> str:
    seed_random()
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{suffix}"


def random_password(length: int = 10) -> str:
    seed_random()
    alphabet = string.ascii_letters + string.digits + "!@#"
    return "".join(random.choices(alphabet, k=length))


def timestamp_slug() -> str:
    return datetime.utcnow().strftime("%Y%m%d%H%M%S")

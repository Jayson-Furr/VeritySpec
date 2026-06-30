from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional

@dataclass
class AccountProfile:
    display_name: str
    age: Optional[int] = None

@dataclass
class AccountContactsItem:
    # Contact email address.
    email: str
    # Whether this is the primary contact.
    primary: Optional[bool] = None

@dataclass
class Account:
    # Stable account identifier.
    id: str
    # Current subscription plan.
    plan: Plan
    # Operational account status.
    status: Literal['active', 'suspended']
    # Searchable account labels.
    tags: Optional[list[str]] = None
    # Public profile details.
    profile: Optional[AccountProfile] = None
    # Account contact methods.
    contacts: Optional[list[AccountContactsItem]] = None
    # Optional display nickname.
    nickname: Optional[str] = None

@dataclass
class Plan:
    # Commercial plan tier.
    tier: Literal['free', 'pro']

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .issues import Issue
from .workspace import Workspace


@dataclass(frozen=True)
class ContractProfile:
    id: str
    name: str
    description: str
    strict: bool
    fail_on: str
    required_packs: tuple[str, ...] = ()
    required_record_kinds: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        data: dict[str, object] = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "strict": self.strict,
            "failOn": self.fail_on,
        }
        if self.required_packs:
            data["requiredPacks"] = list(self.required_packs)
        if self.required_record_kinds:
            data["requiredRecordKinds"] = list(self.required_record_kinds)
        return data


PROFILES: dict[str, ContractProfile] = {
    "release": ContractProfile(
        id="release",
        name="Release",
        description="Strict release-gate enforcement for shippable product contracts.",
        strict=True,
        fail_on="error",
    ),
    "strict": ContractProfile(
        id="strict",
        name="Strict",
        description="Strict validation, lint, and readiness enforcement.",
        strict=True,
        fail_on="error",
    ),
    "regulated": ContractProfile(
        id="regulated",
        name="Regulated",
        description="Strict release enforcement with governance pack coverage.",
        strict=True,
        fail_on="error",
        required_packs=(
            "verity.pack.security",
            "verity.pack.accessibility",
            "verity.pack.compliance",
        ),
    ),
    "public-api": ContractProfile(
        id="public-api",
        name="Public API",
        description="Strict public API enforcement requiring API pack and endpoint records.",
        strict=True,
        fail_on="error",
        required_packs=("verity.pack.api",),
        required_record_kinds=("api.endpoint",),
    ),
    "internal-tool": ContractProfile(
        id="internal-tool",
        name="Internal Tool",
        description="Permissive internal-tool enforcement where warnings remain advisory.",
        strict=False,
        fail_on="error",
    ),
}

PROFILE_CHOICES = tuple(PROFILES)


@dataclass(frozen=True)
class EffectiveProfile:
    profile: ContractProfile | None
    strict: bool
    fail_on: str

    def to_dict(self) -> dict | None:
        if self.profile is None:
            return None
        data = self.profile.to_dict()
        data["effectiveStrict"] = self.strict
        data["effectiveFailOn"] = self.fail_on
        return data


def resolve_profile(
    profile_id: str | None,
    *,
    strict: bool = False,
    fail_on: str | None = None,
) -> EffectiveProfile:
    profile = PROFILES.get(profile_id) if profile_id else None
    return EffectiveProfile(
        profile=profile,
        strict=strict or bool(profile.strict if profile else False),
        fail_on=fail_on or (profile.fail_on if profile else "error"),
    )


def _location(workspace: Workspace) -> str | None:
    return str(workspace.config_path) if workspace.config_path else str(workspace.base_path)


def profile_issues(workspace: Workspace, profile: ContractProfile | None) -> list[Issue]:
    if profile is None:
        return []

    issues: list[Issue] = []
    pack_ids = set(workspace.pack_ids)
    record_kinds = {record.kind for record in workspace.records if record.kind}

    for pack_id in profile.required_packs:
        if pack_id not in pack_ids:
            issues.append(
                Issue(
                    "error",
                    "profile.required_pack",
                    f"Profile '{profile.id}' requires pack '{pack_id}'.",
                    _location(workspace),
                )
            )

    for kind in profile.required_record_kinds:
        if kind not in record_kinds:
            issues.append(
                Issue(
                    "error",
                    "profile.required_record_kind",
                    f"Profile '{profile.id}' requires at least one '{kind}' record.",
                    _location(workspace),
                )
            )

    return issues


def profile_summaries(profiles: Iterable[ContractProfile] = PROFILES.values()) -> list[dict]:
    return [profile.to_dict() for profile in profiles]

"""
S9: Reusable cross-field rule engine.

Usage
-----
Define rules as a list of (condition_fn, field, message) triples where
``condition_fn(data) -> bool`` returns True when the rule is *violated*.

    rules = [
        (lambda d: not d.get("primary_diagnosis"), "primary_diagnosis", "Required."),
    ]
    apply_rules(data, rules)   # raises ValidationError if any rule fires

``apply_rules`` collects *all* violations before raising so that callers
receive the full set of errors in a single response.
"""

from dataclasses import dataclass
from typing import Callable

from rest_framework import serializers


@dataclass
class RuleViolation:
    """Represents a single failed rule."""

    field: str
    message: str


def apply_rules(data: dict, rules: list[tuple[Callable[[dict], bool], str, str]]) -> None:
    """Evaluate every rule against *data* and raise if any are violated.

    Parameters
    ----------
    data:
        The validated (but not yet cross-field-checked) serializer data dict.
    rules:
        An iterable of ``(condition_fn, field, message)`` tuples.
        ``condition_fn(data)`` must return a truthy value when the rule is
        violated.

    Raises
    ------
    rest_framework.serializers.ValidationError
        A single error whose detail is a dict mapping field names to lists of
        error message strings.  All violations are collected before raising so
        the caller sees every problem at once.
    """
    violations: list[RuleViolation] = []

    for condition_fn, field, message in rules:
        try:
            violated = bool(condition_fn(data))
        except Exception:
            # A buggy predicate should not silently pass — treat as violated.
            violated = True
        if violated:
            violations.append(RuleViolation(field=field, message=message))

    if not violations:
        return

    # Build a dict keyed by field so errors group naturally.
    error_dict: dict[str, list[str]] = {}
    for v in violations:
        error_dict.setdefault(v.field, []).append(v.message)

    raise serializers.ValidationError(error_dict)

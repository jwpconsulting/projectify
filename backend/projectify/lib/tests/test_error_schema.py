# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Test error schema generation."""

import pytest
from rest_framework import serializers
from rest_framework.serializers import Serializer

from projectify.lib.error_schema import make_schema


@pytest.fixture
def simple_serializer() -> Serializer:
    """Generate a simple serializer."""

    class SimpleSerializer(Serializer):
        """A simple serializer."""

        text = serializers.CharField()
        number = serializers.IntegerField()

    return SimpleSerializer()


@pytest.fixture
def complex_serializer() -> Serializer:
    """Generate a complex serializer."""

    class NestedSerializer(Serializer):
        """Serializer for a nested field."""

        text = serializers.CharField()

    class ComplexSerializer(Serializer):
        """A complex serializer with many kinds of fields."""

        nested_plural = NestedSerializer(many=True)
        nested_singular = NestedSerializer()
        text_list = serializers.ListField(child=serializers.CharField())
        dict_field = serializers.DictField()
        text = serializers.CharField()

    return ComplexSerializer()


def test_make_schema_simple(simple_serializer: Serializer) -> None:
    """Test make_schema with simple serializer."""
    assert make_schema(simple_serializer) == {
        "type": "object",
        "description": "Error schema",
        "properties": {
            "details": {
                "type": "object",
                "description": "Errors for SimpleSerializer",
                "properties": {
                    "text": {"type": "string"},
                    "number": {"type": "string"},
                },
            },
            "status": {"type": "string", "enum": ["invalid"]},
            "code": {"type": "integer", "enum": [400]},
            "general": {"type": "string"},
        },
        "required": [
            "code",
            "details",
            "status",
        ],
    }


def test_make_schema_complex(complex_serializer: Serializer) -> None:
    """Test make_schema with complex serializer."""
    assert make_schema(complex_serializer) == {
        "type": "object",
        "description": "Error schema",
        "properties": {
            "details": {
                "type": "object",
                "description": "Errors for ComplexSerializer",
                "properties": {
                    "nested_plural": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "description": "Errors for NestedSerializer",
                            "properties": {"text": {"type": "string"}},
                        },
                    },
                    "nested_singular": {
                        "type": "object",
                        "description": "Errors for NestedSerializer",
                        "properties": {"text": {"type": "string"}},
                    },
                    "text_list": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "dict_field": {"type": "string"},
                    "text": {"type": "string"},
                },
            },
            "status": {"type": "string", "enum": ["invalid"]},
            "code": {"type": "integer", "enum": [400]},
            "general": {"type": "string"},
        },
        "required": [
            "code",
            "details",
            "status",
        ],
    }

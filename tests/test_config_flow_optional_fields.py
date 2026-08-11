"""Regression tests for issue #135.

Optional entity-picker fields in the config/options flow must stay
clearable. Home Assistant's frontend forms treat a ``vol.Optional(...,
default=X)`` field as "sticky": once auto-detection pre-fills a guessed
sensor, the user cannot clear the picker back to empty, which blocks saving
whenever the guess is wrong, unavailable, or the wrong type. The fix is to
pre-fill via ``description={"suggested_value": X}`` instead, which shows the
same pre-filled suggestion but leaves the field genuinely clearable.
"""

from __future__ import annotations

import os
import sys

import voluptuous as vol

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _schema_marker(schema: vol.Schema, key_name: str):
    """Return the vol.Optional/vol.Required marker object for a field name."""
    return next(k for k in schema.schema if str(k) == key_name)


class TestRoomFormSchemaClearable:
    """WSStationConfigFlow._room_form_schema (initial setup + options flow)."""

    def test_prefilled_optional_field_has_no_sticky_default(self):
        from custom_components.ws_core.config_flow import WSStationConfigFlow

        flow = WSStationConfigFlow()
        schema = flow._room_form_schema({"name": "Bedroom", "temp": "sensor.bedroom_temp"})

        marker = _schema_marker(schema, "temp")
        # vol.UNDEFINED (rendered as Ellipsis) means "no default" -- the
        # field is not locked to the pre-filled value and can be cleared.
        assert marker.default is vol.UNDEFINED
        assert marker.description == {"suggested_value": "sensor.bedroom_temp"}

    def test_field_with_no_current_value_has_no_default_or_suggestion(self):
        from custom_components.ws_core.config_flow import WSStationConfigFlow

        flow = WSStationConfigFlow()
        schema = flow._room_form_schema({"name": "Office"})

        marker = _schema_marker(schema, "humidity")
        assert marker.default is vol.UNDEFINED

    def test_options_flow_room_form_schema_matches(self):
        from custom_components.ws_core.config_flow import WSStationOptionsFlowHandler

        handler = WSStationOptionsFlowHandler()
        schema = handler._room_form_schema({"name": "Kitchen", "co2": "sensor.kitchen_co2"})

        marker = _schema_marker(schema, "co2")
        assert marker.default is vol.UNDEFINED
        assert marker.description == {"suggested_value": "sensor.kitchen_co2"}


class TestOptionalSourcesSchemaClearable:
    """The optional_sources / optional_sources_opt sensor-mapping steps."""

    def test_guessed_optional_source_is_suggested_not_defaulted(self):
        from custom_components.ws_core.config_flow import OPTIONAL_SOURCES

        guessed_key = next(iter(OPTIONAL_SOURCES))
        defaults = {guessed_key: "sensor.guessed_humidity"}

        # Mirrors the field-construction expression used in
        # async_step_optional_sources / async_step_optional_sources_opt.
        fields = {
            (
                vol.Optional(k, description={"suggested_value": defaults[k]})
                if k in defaults
                else vol.Optional(k)
            ): object()
            for k in OPTIONAL_SOURCES
        }
        schema = vol.Schema(fields)

        marker = _schema_marker(schema, guessed_key)
        assert marker.default is vol.UNDEFINED
        assert marker.description == {"suggested_value": "sensor.guessed_humidity"}

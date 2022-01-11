"""Tests for the Ecobee binary sensor drycontact device."""
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_WINDOW,
    DOMAIN as BINARY_SENSOR_DOMAIN,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_FRIENDLY_NAME,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.helpers import entity_registry as er
from .common import setup_platform
import pytest
from tests.common import load_fixture
import json


@pytest.fixture(scope="function")
def first_requests_mock_fixture(requests_mock):
    vals = {
        "reportList": [{"thermostatIdentifier": "8675309"}],
        "sensorList": [
            {
                "thermostatIdentifier": "8675309",
                "sensors": [
                    {
                        "sensorId": "rs:100:1",
                        "sensorName": "Remote Sensor 1",
                        "sensorType": "temperature",
                        "sensorUsage": "indoor",
                    },
                    {
                        "sensorId": "rs:100:2",
                        "sensorName": "Remote Sensor 2",
                        "sensorType": "occupancy",
                        "sensorUsage": "monitor",
                    },
                    {
                        "sensorId": "dw:100:3",
                        "sensorName": "main door",
                        "sensorType": "dryContact",
                        "sensorUsage": "monitor",
                    },
                ],
                "columns": ["date", "time", "rs:100:1", "rs:100:2", "dw:100:3"],
                "data": [
                    "2022-01-09,18:35:00,78.2,0,1",
                    "2022-01-09,18:49:00,78.2,0,1",
                    "2022-01-09,18:45:00,78.2,0,1",
                    "2022-01-09,18:50:00,78.2,0,1",
                    "2022-01-09,18:55:00,78.2,0,1",
                    "2022-01-09,19:00:00,78.2,0,1",
                    "2022-01-09,19:05:00,78.2,0,0",
                    "2022-01-09,19:10:00,78.2,0,1",
                    "2022-01-09,19:15:00,,,",
                ],
            }
        ],
    }

    requests_mock.get("https://api.ecobee.com/1/runtimeReport", text=json.dumps(vals))


@pytest.fixture(scope="function")
def update_requests_mock_fixture(requests_mock):
    vals = {
        "reportList": [{"thermostatIdentifier": "8675309"}],
        "sensorList": [
            {
                "thermostatIdentifier": "8675309",
                "sensors": [
                    {
                        "sensorId": "rs:100:1",
                        "sensorName": "Remote Sensor 1",
                        "sensorType": "temperature",
                        "sensorUsage": "indoor",
                    },
                    {
                        "sensorId": "rs:100:2",
                        "sensorName": "Remote Sensor 2",
                        "sensorType": "occupancy",
                        "sensorUsage": "monitor",
                    },
                    {
                        "sensorId": "dw:100:3",
                        "sensorName": "main door",
                        "sensorType": "dryContact",
                        "sensorUsage": "monitor",
                    },
                ],
                "columns": ["date", "time", "rs:100:1", "rs:100:2", "dw:100:3"],
                "data": [
                    "2022-01-09,18:35:00,78.2,0,1",
                    "2022-01-09,18:49:00,78.2,0,1",
                    "2022-01-09,18:45:00,78.2,0,1",
                    "2022-01-09,18:50:00,78.2,0,1",
                    "2022-01-09,18:55:00,78.2,0,1",
                    "2022-01-09,19:00:00,78.2,0,1",
                    "2022-01-09,19:05:00,78.2,0,0",
                    "2022-01-09,19:10:00,78.2,0,1",
                    "2022-01-09,19:15:00,78.2,0,1",
                    "2022-01-09,19:20:00,78.2,0,0",
                    "2022-01-09,19:25:00,78.2,0,1",
                    "2022-01-09,19:30:00,78.2,1,0",
                    "2022-01-09,19:35:00,,,",
                ],
            }
        ],
    }

    requests_mock.get("https://api.ecobee.com/1/runtimeReport", text=json.dumps(vals))


async def test_entity_registry(first_requests_mock_fixture, hass):
    """Tests the drycontact devices are registered in the entity registry."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("binary_sensor.main_door_drycontact")

    assert entry.unique_id == "8675309-dw:100:3"
    assert entry.original_name == "main door DryContact"


async def test_attributes(first_requests_mock_fixture, hass):
    """Test the drycontact binary sensor attributes are correct."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)
    state = hass.states.get("binary_sensor.main_door_drycontact")

    assert state.state == STATE_OFF
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "main door DryContact"
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_WINDOW
    assert state.attributes.get("date") == "2022-01-09"
    assert state.attributes.get("time") == "19:10:00"


async def test_update_attributes(update_requests_mock_fixture, hass):
    """Test the drycontact binary sensor attributes are updated."""
    await setup_platform(hass, BINARY_SENSOR_DOMAIN)
    state = hass.states.get("binary_sensor.main_door_drycontact")

    assert state.state == STATE_ON
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "main door DryContact"
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_WINDOW
    assert state.attributes.get("date") == "2022-01-09"
    assert state.attributes.get("time") == "19:30:00"

"""Support for WLED button."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ENTITY_CATEGORY_CONFIG
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import WLEDDataUpdateCoordinator
from .helpers import wled_exception_handler
from .models import WLEDEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up WLED button based on a config entry."""
    coordinator: WLEDDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WLEDRestartButton(coordinator)])


class WLEDRestartButton(WLEDEntity, ButtonEntity):
    """Defines a WLED restart switch."""

    _attr_icon = "mdi:restart"
    _attr_entity_category = ENTITY_CATEGORY_CONFIG

    def __init__(self, coordinator: WLEDDataUpdateCoordinator) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator=coordinator)
        self._attr_name = f"{coordinator.data.info.name} Restart"
        self._attr_unique_id = f"{coordinator.data.info.mac_address}_restart"

    @wled_exception_handler
    async def async_press(self) -> None:
        """Send out a restart command."""
        await self.coordinator.wled.reset()

from typing import Annotated
from semantic_kernel.functions import kernel_function

class ACControlPlugin:
    """A plugin to control the Air Conditioner (AC)."""
    
    @kernel_function(description="Turn the air conditioner on or off.")
    def control_device_operation(self, operation: Annotated[str, "The operation to perform (on/off)."]) -> str:
        if operation == "on":
            return "Air conditioner turned on."
        elif operation == "off":
            return "Air conditioner turned off."
        return "Invalid operation for air conditioner."

    @kernel_function(description="Set the air conditioner temperature.")
    def set_temperature(self, temperature: Annotated[str, "The temperature to set."]) -> str:
        return f"Air conditioner temperature set to {temperature} degrees."

    @kernel_function(description="Adjust the air conditioner temperature.")
    def adjust_temperature(self, operation: Annotated[str, "Increase or decrease temperature."], value: Annotated[str, "Value to adjust by."]) -> str:
        return f"Air conditioner temperature {operation}d by {value} degrees."

    @kernel_function(description="Set the air conditioner mode.")
    def set_mode(self, mode: Annotated[str, "The mode (cool, fan, dry)."]) -> str:
        return f"Air conditioner set to {mode} mode."

    @kernel_function(description="Set the air conditioner timer.")
    def set_timer(self, time: Annotated[str, "Duration for timer (e.g., 2 hours)."]) -> str:
        return f"Air conditioner timer set to {time}."


class TVControlPlugin:
    """A plugin to control the TV."""
    
    @kernel_function(description="Turn the TV on or off.")
    def control_device_operation(self, operation: Annotated[str, "Turn TV on or off."]) -> str:
        return f"TV turned {operation}."

    @kernel_function(description="Adjust TV volume.")
    def adjust_volume(self, operation: Annotated[str, "Increase or decrease volume."]) -> str:
        return f"TV volume {operation}d."

    @kernel_function(description="Switch TV input source.")
    def switch_input_source(self, input_source: Annotated[str, "Input source (e.g., HDMI 1, HDMI 2)."]) -> str:
        return f"TV input switched to {input_source}."

    @kernel_function(description="Open an app on the TV.")
    def open_application(self, app_name: Annotated[str, "App to open on the TV."]) -> str:
        return f"{app_name} opened on the TV."

    @kernel_function(description="Set TV brightness.")
    def set_brightness(self, brightness: Annotated[str, "Brightness level."]) -> str:
        return f"TV brightness set to {brightness}."

    @kernel_function(description="Set TV channel.")
    def set_channel(self, channel: Annotated[str, "Channel number."]) -> str:
        return f"TV channel set to {channel}."

    @kernel_function(description="Enable subtitles on the TV.")
    def enable_subtitles(self) -> str:
        return "Subtitles enabled on the TV."


class RefrigeratorControlPlugin:
    """A plugin to control the refrigerator."""
    
    @kernel_function(description="Set refrigerator temperature.")
    def set_temperature(self, temperature: Annotated[str, "Desired temperature."]) -> str:
        return f"Refrigerator temperature set to {temperature} degrees."

    @kernel_function(description="Enable or disable refrigerator power-saving mode.")
    def toggle_power_saving_mode(self, operation: Annotated[str, "Enable or disable mode."]) -> str:
        return f"Refrigerator power-saving mode {operation}d."


class DishwasherControlPlugin:
    """A plugin to control the dishwasher."""
    
    @kernel_function(description="Start, stop, pause, or resume the dishwasher.")
    def control_device_operation(self, operation: Annotated[str, "Operation to perform."]) -> str:
        return f"Dishwasher {operation}d."

    @kernel_function(description="Set the dishwasher mode.")
    def set_mode(self, mode: Annotated[str, "Dishwasher mode (e.g., eco, heavy wash)."]) -> str:
        return f"Dishwasher set to {mode} mode."

    @kernel_function(description="Set the dishwasher timer.")
    def set_timer(self, time: Annotated[str, "Timer duration (e.g., 1 hour)."]) -> str:
        return f"Dishwasher timer set to {time}."


class WashingMachineControlPlugin:
    """A plugin to control the washing machine."""
    
    @kernel_function(description="Start, stop, pause, or resume the washing machine.")
    def control_device_operation(self, operation: Annotated[str, "Operation to perform (start/stop/pause/resume). "]) -> str:
        return f"Washing machine {operation}."
    
    @kernel_function(description="Set the washing machine mode.")
    def set_mode(self, mode: Annotated[str, "The mode to set (quick wash, delicate, heavy load). "]) -> str:
        return f"Washing machine set to {mode} mode."
    
    @kernel_function(description="Set the washing machine timer.")
    def set_timer(self, time: Annotated[str, "Timer duration (e.g., 30 minutes, 1 hour). "]) -> str:
        return f"Washing machine timer set to {time}."

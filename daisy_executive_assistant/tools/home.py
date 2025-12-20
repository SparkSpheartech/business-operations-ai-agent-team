import json
from googleapiclient.errors import HttpError
from daisy_executive_assistant.tools.auth import get_home_service, get_project_id

def list_smart_home_devices() -> str:
    """Lists all accessible Google Home/Nest devices."""
    try:
        service = get_home_service()
        project_id = get_project_id()
        parent = f"enterprises/{project_id}"
        
        results = service.enterprises().devices().list(parent=parent).execute()
        devices = results.get('devices', [])

        if not devices:
            return 'No devices found. (Ensure you have linked the project in Device Access Console)'

        output = []
        for dev in devices:
            name = dev.get('name', 'Unknown')
            dev_type = dev.get('type', 'Unknown Device')
            traits = dev.get('traits', {})
            info = traits.get('sdm.devices.traits.Info', {})
            custom_name = info.get('customName', 'No Name')
            output.append(f"Name: {custom_name} | Type: {dev_type} | ID: {name}")
        
        return "\\n".join(output)

    except HttpError as error:
        return f'An error occurred listing devices: {error}'

def execute_device_command(device_id: str, command: str, params_json: str = "{}") -> str:
    """Executes a command on a smart device.
    device_id: Full resource name.
    command: Command name (e.g. sdm.devices.commands...).
    params_json: JSON string of parameters (e.g. '{"heatCelsius": 22}').
    """
    try:
        service = get_home_service()
        try:
            params = json.loads(params_json)
        except json.JSONDecodeError:
            return "Error: params_json must be a valid JSON string."

        body = {
            'command': command,
            'params': params
        }
        service.enterprises().devices().executeCommand(
            name=device_id, body=body).execute()
        return f"Command '{command}' executed successfully."

    except HttpError as error:
        return f'An error occurred executing command: {error}'

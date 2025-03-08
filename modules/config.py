import json
from modules.constants import CONFIG_FILE_LOCATION, LOADSHEDDING_FILE_LOCATION, get_version

class ConfigManager:
    def __init__(self):
        ensure_directories()  # Ensure directories and files are created
        self.config_file = CONFIG_FILE_LOCATION
        self.loadshedding_file = LOADSHEDDING_FILE_LOCATION
        self.config = self.load_config(self.config_file)
        self.loadshedding_config = self.load_config(self.loadshedding_file)
        self.config['version'] = get_version()  # Include the dynamic version in the config

    def load_config(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return {}

    def save_config(self, file_path, data):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving config to file: {file_path}, Error: {e}")

    def get_config(self):
        return self.config

    def get_loadshedding_config(self):
        return self.loadshedding_config

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config(self.config_file, self.config)

    def update_loadshedding_config(self, key, value):
        self.loadshedding_config[key] = value
        self.save_config(self.loadshedding_file, self.loadshedding_config)

    # Methods to set data
    def set_province_id(self, province_id):
        self.update_loadshedding_config('province_id', province_id)

    def set_municipal_id(self, municipal_id):
        self.update_loadshedding_config('municipal_id', municipal_id)

    def set_suburb_id(self, suburb_id):
        self.update_loadshedding_config('suburb_id', suburb_id)

    def set_location_id(self, location_id):
        self.update_config('location_id', location_id)

    def set_longitude(self, longitude):
        self.update_config('longitude', longitude)

    def set_latitude(self, latitude):
        self.update_config('latitude', latitude)

    def set_api_token(self, api_token):
        self.update_config('api_token', api_token)

    def set_current_stage(self, stage, source):
        key = f'current_stage_{source}'
        self.update_loadshedding_config(key, stage)

    def set_current_schedule(self, schedule, source):
        key = f'current_schedule_{source}'
        self.update_loadshedding_config(key, schedule)

    def set_area_info(self, area_info):
        self.update_loadshedding_config('area_info', area_info)

    # Methods to get data
    def get_province_id(self):
        return self.loadshedding_config.get('province_id')

    def get_municipal_id(self):
        return self.loadshedding_config.get('municipal_id')

    def get_suburb_id(self):
        return self.loadshedding_config.get('suburb_id')

    def get_location_id(self):
        return self.config.get('location_id')

    def get_longitude(self):
        return self.config.get('longitude')

    def get_latitude(self):
        return self.config.get('latitude')

    def get_api_token(self):
        return self.config.get('api_token')

    def get_current_stage(self, source):
        key = f'current_stage_{source}'
        return self.loadshedding_config.get(key)

    def get_current_schedule(self, source):
        key = f'current_schedule_{source}'
        return self.loadshedding_config.get(key)

    def get_area_info(self):
        return self.loadshedding_config.get('area_info')

    def create_notification(self, name, time_offset, notification_type, offset_type="before", shutdown_delay=None):
        if 'notifications' not in self.loadshedding_config:
            self.loadshedding_config['notifications'] = {}

        self.loadshedding_config['notifications'][name] = {
            'time_offset': time_offset,
            'type': notification_type,
            'offset_type': offset_type
        }

        if shutdown_delay is not None:
            self.loadshedding_config['notifications'][name]['shutdown_delay'] = shutdown_delay

        self.save_config(self.loadshedding_file, self.loadshedding_config)

    def update_notification(self, name, time_offset=None, notification_type=None, offset_type=None,
                            shutdown_delay=None):
        if 'notifications' not in self.loadshedding_config or name not in self.loadshedding_config['notifications']:
            print(f"Notification '{name}' not found.")
            return

        if time_offset is not None:
            self.loadshedding_config['notifications'][name]['time_offset'] = time_offset

        if notification_type is not None:
            self.loadshedding_config['notifications'][name]['type'] = notification_type

        if offset_type is not None:
            self.loadshedding_config['notifications'][name]['offset_type'] = offset_type

        if shutdown_delay is not None:
            self.loadshedding_config['notifications'][name]['shutdown_delay'] = shutdown_delay

        self.save_config(self.loadshedding_file, self.loadshedding_config)

    def read_notification(self, name):
        return self.loadshedding_config.get('notifications', {}).get(name)

    def delete_notification(self, name):
        if 'notifications' in self.loadshedding_config and name in self.loadshedding_config['notifications']:
            del self.loadshedding_config['notifications'][name]
            self.save_config(self.loadshedding_file, self.loadshedding_config)


from modules.config import ConfigManager

def main():
    config_manager = ConfigManager()

    # Set data
    config_manager.set_province_id(1)
    config_manager.set_municipal_id(101)
    config_manager.set_suburb_id(1000001)
    config_manager.set_location_id('capetown-6-vanriebeeckshof')
    config_manager.set_longitude(18.423300)
    config_manager.set_latitude(-33.918861)
    config_manager.set_api_token('YOUR_API_TOKEN')

    # Set current stage and schedule
    config_manager.set_current_stage(3, 'thespear')
    config_manager.set_current_stage(3, 'esp')
    config_manager.set_current_schedule('schedule data for thespear', 'thespear')
    config_manager.set_current_schedule('schedule data for esp', 'esp')
    config_manager.set_area_info('Area info data')

    # Create, read, update, and delete notifications
    config_manager.create_notification("notify_before_15", 15, "tray", "before")
    config_manager.create_notification("notify_before_5_shutdown", 5, "shutdown", "before", shutdown_delay=60)
    print("Created Notifications:", config_manager.loadshedding_config['notifications'])

    notification_before_15 = config_manager.read_notification("notify_before_15")
    print("Read Notification 'notify_before_15':", notification_before_15)

    config_manager.update_notification("notify_before_15", time_offset=10)
    updated_notification_before_15 = config_manager.read_notification("notify_before_15")
    print("Updated Notification 'notify_before_15':", updated_notification_before_15)

    config_manager.delete_notification("notify_before_15")
    print("Notifications after deletion:", config_manager.loadshedding_config['notifications'])

    # Get data
    print("Province ID:", config_manager.get_province_id())
    print("Municipal ID:", config_manager.get_municipal_id())
    print("Suburb ID:", config_manager.get_suburb_id())
    print("Location ID:", config_manager.get_location_id())
    print("Longitude:", config_manager.get_longitude())
    print("Latitude:", config_manager.get_latitude())
    print("API Token:", config_manager.get_api_token())
    print("Current Stage (thespear):", config_manager.get_current_stage('thespear'))
    print("Current Stage (esp):", config_manager.get_current_stage('esp'))
    print("Current Schedule (thespear):", config_manager.get_current_schedule('thespear'))
    print("Current Schedule (esp):", config_manager.get_current_schedule('esp'))
    print("Area Info:", config_manager.get_area_info())

if __name__ == "__main__":
    main()

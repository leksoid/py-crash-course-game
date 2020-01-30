class Settings:
    """Use to store all settings for AI game"""

    def __init__(self):
        # Initialize game settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        #Alien settings
        self.alien_speed = 1.0
        self.alien_drop_speed = 10
        self.fleet_direction = 1 # 1 = right , -1 = left

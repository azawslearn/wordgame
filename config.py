import configparser

# Reading config.cfg file
config = configparser.ConfigParser()
config.read('config.cfg')

# Database configurations
DB_USERNAME = "ivansto"
DB_PASSWORD = "EmersonFitipaldi"
DB_HOST = config.get('Database', 'DB_HOST', fallback='default_value_if_not_set')
DB_NAME = "words"

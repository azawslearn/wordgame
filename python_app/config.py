import configparser

# Initialize the config parser
config = configparser.ConfigParser()

# Read the config.cfg file from the full path
config.read('/home/ubuntu/config.cfg')

# Database configurations
DB_USERNAME = "ivansto"
DB_PASSWORD = "EmersonFitipaldi"
DB_HOST = config.get('Database', 'DB_HOST', fallback='default_value_if_not_set')
DB_NAME = "words"

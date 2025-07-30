import configparser

config = configparser.ConfigParser()
config.read('database.ini')

DB_USERNAME = config['mysql']['username']
DB_PASSWORD = config['mysql']['password']
DB_NAME = config['mysql']['database']

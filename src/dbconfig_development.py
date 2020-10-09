DEVELOPMENT = True
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(**{
    'user':     'postgres',
    'password': 'postgres',
    'host':     'postgres-server',
    'port':     '5432',
    'db':     'postgres'
})

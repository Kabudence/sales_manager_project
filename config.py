class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///business.db'  # Aquí se define la URI de la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'
    JWT_SECRET_KEY = 'supersecretkey'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Expiración del token en segundos

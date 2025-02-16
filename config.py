from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qZstrAoIqsucmseTmCeklUyhPOBLLohs@crossover.proxy.rlwy.net:37524/railway"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'e04c4e87a50b5e0f790cb7006480b303ddf5aded8a1c7e09ded3570515005e10'
    JWT_SECRET_KEY = 'a25fc7905471e60a094749de707ab956871d5ba26df167a03863911a70c54950'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=770)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
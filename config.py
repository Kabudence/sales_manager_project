from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:gitano200J%40%40J%40%40@localhost:3306/hidadata'
    SQLALCHEMY_TRACK_MODIFICATIONS = FalseSECRET_KEY = 'e04c4e87a50b5e0f790cb7006480b303ddf5aded8a1c7e09ded3570515005e10'
    JWT_SECRET_KEY = 'a25fc7905471e60a094749de707ab956871d5ba26df167a03863911a70c54950'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=770)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
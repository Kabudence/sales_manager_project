class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:gitano200J%40%40J%40%40@localhost:3306/hidata'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'
    JWT_SECRET_KEY = 'supersecretkey'
    JWT_ACCESS_TOKEN_EXPIRES = 3600

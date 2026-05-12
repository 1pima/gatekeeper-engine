from flask_sqlalchemy import SQLAlchemy

dbc = SQLAlchemy()

import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore', category=SAWarning)

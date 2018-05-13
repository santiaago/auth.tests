'fake database for demo purposes'
import logging

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s [%(process)d] [%(levelname)s] %(name)s:%(funcName)s - %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S %z]")
handler.setFormatter(formatter)
logger.addHandler(handler)

class FakeDatabase:
    def __init__(self):
        logger.info('initializing database')
        self.database = list()
    
    def get_user(self, id):
        logger.info('looking for user %s', id)
        matches = filter(lambda user: user.id == id,self.database)
        return matches

    def insert_user(self, user):
        logger.info('inserting user %s', user)
        matches = filter( lambda user: user.id == id, self.database)
        if not matches:
            self.database.append(user)
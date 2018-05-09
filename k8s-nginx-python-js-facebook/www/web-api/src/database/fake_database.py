'fake database for demo purposes'

class FakeDatabase:
    def __init__(self):
        self.database = list()
    
    def get_user(self, id):
        matches = filter(lambda user: user.id == id,self.database)
        return matches

    def insert_user(self, user):
        matches = filter( lambda user: user.id == id, self.database)
        if not matches:
            self.database.append(user)
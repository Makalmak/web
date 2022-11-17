class UserLogin:

    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def getName(self):
        return self.__user[1] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user[4] if self.__user else "Без email"

    def getLogin(self):
        return self.__user[2]
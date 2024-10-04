from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base



class UserDB:
    Base = declarative_base() #base class that table schema classes inehrit from

    engine = create_engine('sqlite:///databases/instance/users.db') #connects sqlalchemy engine to database file
    Session = sessionmaker(bind=engine) #binds session to engine
    session = Session() #creates session object

    class User(Base): #inherits from declarative_base object to define how a table is structured
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String)
        email = Column(String)
        password = Column(String)

    
    def add_user(self, username: str, email: str, password: str): #adds a user
        if username and password:
            new_user = self.User(username=username, email=email, password=password)
            self.session.add(new_user) #adds user object
            self.session.commit() #commits changes to file
        else:
            print("add_user: Missing username or password, no user added")

    def find_users(self, username: str): #returns a list of dictionaries, one for each user
        #structure = session.query(table object).filter(operation on column object inside table object).all()/.first()

        if username:
            result = self.session.query(self.User).filter(self.User.username == username).all()
        else:
            print("find_user: No username passed in")
            return []

        user_list = [user.__dict__ for user in result] #converts all returned user objects to dictionary

        for user_dict in user_list: #remove useless SQLAlchemy metadata from dictionaries
            user_dict.pop('_sa_instance_state',None)

        return user_list #returns all users matching the specified query (ideally 0 or 1, can be more but shouldnt)
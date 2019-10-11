from app.utils.extensions.database import module as connector



class ServicePath(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 


    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))

    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()


class AgeGroup(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 

    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()


class UnemploymentDuration(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()



class Health(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()


class Immigration(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()


class Target(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()


class Study(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()


class Classification(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()

class Integration(connector.Model):
    __table_args__                  = {
                                        'extend_existing': True
                                    } 
                        
    id                              = connector.Column(connector.Integer, primary_key=True)
    text                            = connector.Column(connector.String(100))
    def __str__(self):
        return self.text

    @staticmethod
    def get_choices():
        return UnemploymentDuration.query.all()




def get_choices(_type):
    if _type == 'asd':
        return UnemploymentDuration.query.all()





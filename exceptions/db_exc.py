from fastapi import HTTPException, Response


class NotFoundException(Exception):
    
    def __init__(self, message='User not found'):
        self.message = message
        super().__init__(self.message)
        raise HTTPException(404, message)
        

class FieldAlredyExist(Exception):

    def __init__(self, message='Email or login alredy exists'):
        self.message = message
        super().__init__(self.message)
        raise HTTPException(400, message)


class NotOwnerException(Exception):

    def __init__(self, event='post'):
        self.message = f'User not owner {event}'
        super().__init__(self.message)
        raise HTTPException(403, self.message)

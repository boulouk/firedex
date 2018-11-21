
from model.publication_collection import PublicationCollection

class PublishersConfiguration:

    def __init__(self):
        self.__publication_collection = PublicationCollection()

    def publication_collection(self):
        return self.__publication_collection

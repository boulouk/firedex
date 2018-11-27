
from model.publication import Publication

class PublicationCollection:

    def __init__(self):
        self.__publications = []

    def publications(self):
        return self.__publications

    def add_publication(self, publisher, topic, rate, message_size):
        publication = Publication(
            publisher = publisher,
            topic = topic,
            rate = rate,
            message_size = message_size
        )

        self.__publications.append(publication)

    def remove_publication(self, publisher, topic):
        dummy_rate = -1
        dummy_size = -1

        publication = Publication(
            publisher = publisher,
            topic = topic,
            rate = dummy_rate,
            message_size = dummy_size
        )

        self.__publications.remove(publication)

    def publications_load_by_topic(self, topic):
        publications = self.publications()
        publications_load_by_topic = sum(publication.publication_load() for publication in publications if publication.topic() == topic)

        return publications_load_by_topic

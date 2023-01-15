import hydrus_api
import hydrus_api.utils
import logging


class Hydrus:
    def __init__(self, access_key: str):
        self.client = hydrus_api.Client(access_key=access_key)
        self.chunk_size = 100
        self.logger = logging.getLogger(__name__)

    def search_tag(self, query):
        tags = query.split(" ")
        self.logger.info(f"Searching by tags: {tags}")
        result = self.client.search_files(tags)
        return result

    def get_thumbnail(self, file_id):
        thumb = self.client.get_thumbnail(file_id=file_id)
        return thumb.content

    def full_size(self, file_id):
        full = self.client.get_file(file_id=file_id)
        return full.content

    def get_metadata(self, file_id):
        metadata = self.client.get_file_metadata(file_ids=[file_id])[0]
        return metadata

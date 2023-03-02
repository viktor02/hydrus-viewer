import sys

import hydrus_api
import hydrus_api.utils
import logging

REQUIRED_PERMISSIONS = {hydrus_api.Permission.SEARCH_FILES}


class Hydrus:
    def __init__(self, access_key: str):
        self.client = hydrus_api.Client(access_key=access_key)
        self.logger = logging.getLogger(__name__)

        if not hydrus_api.utils.verify_permissions(self.client, REQUIRED_PERMISSIONS):
            self.logger.error("The API key does not grant all required permissions:", REQUIRED_PERMISSIONS)
            sys.exit(-1)

    def get_page(self, query, number, only_archived=True):
        tags = query.split(",")
        tags = [i.strip() for i in tags]

        self.logger.debug(f"Searching page {number} by tags: {tags}")
        if only_archived:
            tags.append("system:archive")
        file_ids = self.client.search_files(tags, file_sort_type=hydrus_api.FileSortType.RANDOM)

        # set the current page number and the number of results per page
        page = number
        per_page = 30

        # calculate the start and end index for the current page
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        # get the file_ids for the current page
        current_page_file_ids = file_ids[start_index:end_index]

        return current_page_file_ids

    def get_thumbnail(self, file_id):
        thumb = self.client.get_thumbnail(file_id=file_id)
        return thumb.content

    def full_size(self, file_id):
        full = self.client.get_file(file_id=file_id)
        return full.content

    def search_tags(self, tag):
        tags = self.client.search_tags(tag)
        return tags[-5:] # returns last 5 tags

    def get_metadata(self, file_id):
        try:
            metadata = self.client.get_file_metadata(file_ids=[file_id])[0]
            return metadata
        except hydrus_api.APIError:
            return None

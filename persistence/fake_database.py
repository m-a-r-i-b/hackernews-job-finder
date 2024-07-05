from logging import exception
from persistence.database_service import DatabaseService


class Database:
    def __init__(self):
        self._table_data = {}
        self._table_data_updated = {}
        self.database_service = DatabaseService()


    def create_project(self, project_id: str, data):
        new_project_data =  self._read_or_create_project(project_id, data)
        self._table_data[project_id] = new_project_data
        return new_project_data


    def get_project(self, project_id: str):
        return self._table_data.get(project_id)
    

    def get_comment(self, project_id: str, comment_id: str):
        return self._table_data.get(project_id)[comment_id]
    

    def update_project(self, project_id: str, data):
        if project_id in self._table_data:
            # Update existing dictionary with new data
            self._table_data[project_id].update(data)
        else:
            # If project_id does not exist, just set it
            self._table_data[project_id] = data

        self._table_data_updated[project_id] = True
        # TODO : Move this to a separate thread
        self._persist_data()


    def update_comment(self, project_id: str, comment_id: str, data):
        if project_id in self._table_data:
            if comment_id in self._table_data[project_id]:
                self._table_data[project_id][comment_id].update(data)
            else:
                self._table_data[project_id][comment_id] = data
        else:
            print('[ERROR] | Project id {project_id} not found...')
            return

        self._table_data_updated[project_id] = True
        # TODO : Move this to a separate thread
        self._persist_data()


    def _read_or_create_project(self, project_id: str, data):
        try:
            project_data = self.database_service.load_project(project_id)
            if project_data is None or not project_data:
                print("Creating new project...")
                project_data = self.database_service.create_or_update_project(project_id, data)

            return project_data
        except exception:
            pass


    def _persist_data(self):
        for project_id, data in self._table_data.items():
            if self._table_data_updated.get(project_id, False):
                self.database_service.create_or_update_project(project_id, data)
                self._table_data_updated[project_id] = False



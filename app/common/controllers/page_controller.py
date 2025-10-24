from app.common.services.page_service import PageService

class PageController:
    def __init__(self):
        self.page_service = PageService()
    
    def get_all_pages(self):
        return self.page_service.get_all_pages()
    
    def get_page_by_id(self, page_id):
        return self.page_service.get_page_by_id(page_id)
    
    def create_page(self, page_data, icon_file=None):
        return self.page_service.create_page(page_data, icon_file)
    
    def update_page(self, page_id, page_data, icon_file=None):
        return self.page_service.update_page(page_id, page_data, icon_file)
    
    def delete_page(self, page_id):
        return self.page_service.delete_page(page_id)
    
    def get_pages_by_application(self, app_id):
        return self.page_service.get_pages_by_application(app_id)
    
    def add_pages_to_application(self, app_id, page_ids):
        return self.page_service.add_pages_to_application(app_id, page_ids)
    
    def remove_pages_from_application(self, app_id, page_ids):
        return self.page_service.remove_pages_from_application(app_id, page_ids) 
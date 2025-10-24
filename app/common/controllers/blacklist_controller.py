from app.common.services.blacklist_service import BlackListService

class BlackListController:
    def __init__(self):
        self.blacklist_service = BlackListService()
    
    def get_all_blacklists(self):
        return self.blacklist_service.get_all_blacklists()
    
    def get_all_blacklists_paginated(self, page, per_page):
        return self.blacklist_service.get_blacklists_paginated(page, per_page)
    
    def get_blacklist_by_id(self, blacklist_id):
        return self.blacklist_service.get_blacklist_by_id(blacklist_id)
    
    def get_blacklist_by_number(self, number):
        return self.blacklist_service.get_blacklist_by_number(number)
    
    def create_blacklist(self, blacklist_data):
        return self.blacklist_service.create_blacklist(blacklist_data)
    
    def update_blacklist(self, blacklist_id, blacklist_data):
        return self.blacklist_service.update_blacklist(blacklist_id, blacklist_data)
    
    def delete_blacklist(self, blacklist_id):
        return self.blacklist_service.delete_blacklist(blacklist_id)
    
    def is_number_blacklisted(self, number):
        return self.blacklist_service.is_number_blacklisted(number)
    
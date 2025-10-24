from app.common.services.trace_service import TraceService

class TraceController:
    def __init__(self):
        self.trace_service = TraceService()
    
    def get_all_traces(self):
        return self.trace_service.get_all_traces()
    
    def get_traces_paginated(self, page, per_page):
        return self.trace_service.get_traces_paginated(page, per_page)
    
    def get_trace_by_id(self, trace_id):
        return self.trace_service.get_trace_by_id(trace_id)
    
    def create_trace(self, trace_data):
        return self.trace_service.create_trace(trace_data)
    
    def update_trace(self, trace_id, trace_data):
        return self.trace_service.update_trace(trace_id, trace_data)
    
    def delete_trace(self, trace_id):
        return self.trace_service.delete_trace(trace_id)
    
    def get_traces_by_utilisateur(self, utilisateur_id):
        return self.trace_service.get_traces_by_utilisateur(utilisateur_id)
    
    def get_traces_by_action(self, action):
        return self.trace_service.get_traces_by_action(action)
    
    def get_traces_by_date_range(self, start_date, end_date):
        return self.trace_service.get_traces_by_date_range(start_date, end_date)
    
    def get_traces_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        return self.trace_service.get_traces_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    def get_traces_by_action_paginated(self, action, page, per_page):
        return self.trace_service.get_traces_by_action_paginated(action, page, per_page)
    
    def get_traces_by_date_range_paginated(self, start_date, end_date, page, per_page):
        return self.trace_service.get_traces_by_date_range_paginated(start_date, end_date, page, per_page) 
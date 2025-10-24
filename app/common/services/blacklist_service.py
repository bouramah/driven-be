from app.common.models import BlackList, db
from datetime import datetime

class BlackListService:
    def get_all_blacklists(self):
        return BlackList.query.all()
    
    def get_blacklists_paginated(self, page, per_page):
        return BlackList.query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_blacklist_by_id(self, blacklist_id):
        return BlackList.query.get(blacklist_id)
    
    def get_blacklist_by_number(self, number):
        return BlackList.query.filter_by(numero=number).first()
    
    def create_blacklist(self, blacklist_data):
        blacklist = BlackList(**blacklist_data)
        if 'date_ajout' not in blacklist_data:
            blacklist.date_ajout = datetime.utcnow()
            
        db.session.add(blacklist)
        db.session.commit()
        return blacklist
    
    def update_blacklist(self, blacklist_id, blacklist_data):
        blacklist = self.get_blacklist_by_id(blacklist_id)
        if not blacklist:
            return None
            
        for key, value in blacklist_data.items():
            setattr(blacklist, key, value)
            
        db.session.commit()
        return blacklist
    
    def delete_blacklist(self, blacklist_id):
        blacklist = self.get_blacklist_by_id(blacklist_id)
        if blacklist:
            db.session.delete(blacklist)
            db.session.commit()
            return True
        return False
    
    def is_number_blacklisted(self, number):
        return bool(self.get_blacklist_by_number(number))
    
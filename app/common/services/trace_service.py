from app.common.models import Trace, db
from datetime import datetime
import json
from flask import request

class TraceService:
    def get_all_traces(self):
        return Trace.query.all()
    
    def get_traces_paginated(self, page, per_page):
        return Trace.query.order_by(Trace.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_trace_by_id(self, trace_id):
        return Trace.query.get(trace_id)
    
    def create_trace(self, trace_data):
        trace = Trace(**trace_data)
        if 'date' not in trace_data:
            trace.date = datetime.utcnow()
            
        db.session.add(trace)
        db.session.commit()
        return trace
    
    def update_trace(self, trace_id, trace_data):
        trace = self.get_trace_by_id(trace_id)
        if not trace:
            return None
            
        for key, value in trace_data.items():
            setattr(trace, key, value)
            
        db.session.commit()
        return trace
    
    def delete_trace(self, trace_id):
        trace = self.get_trace_by_id(trace_id)
        if trace:
            db.session.delete(trace)
            db.session.commit()
            return True
        return False
    
    def get_traces_by_utilisateur(self, utilisateur_id):
        return Trace.query.filter_by(id_utilisateur=utilisateur_id).order_by(Trace.date.desc()).all()
    
    def get_traces_by_action(self, action):
        return Trace.query.filter_by(action=action).order_by(Trace.date.desc()).all()
    
    def get_traces_by_date_range(self, start_date, end_date):
        return Trace.query.filter(
            Trace.date >= start_date,
            Trace.date <= end_date
        ).order_by(Trace.date.desc()).all()
    
    def get_traces_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        return Trace.query.filter_by(id_utilisateur=utilisateur_id).order_by(Trace.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_traces_by_action_paginated(self, action, page, per_page):
        return Trace.query.filter_by(action=action).order_by(Trace.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_traces_by_date_range_paginated(self, start_date, end_date, page, per_page):
        return Trace.query.filter(
            Trace.date >= start_date,
            Trace.date <= end_date
        ).order_by(Trace.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def ajouter_trace(action, detail, code, id_utilisateur=None, params=None, code_sql=None):
        """Ajouter une nouvelle trace"""
        try:
            trace = Trace(
                date=datetime.utcnow(),
                action=action,
                detail=detail,
                code=code,
                param=json.dumps(params) if params else None,
                code_sql=code_sql,
                end_point=request.path,
                id_utilisateur=id_utilisateur
            )
            
            db.session.add(trace)
            db.session.commit()
            return trace
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'ajout de la trace: {str(e)}")
            # On ne lève pas l'exception pour ne pas bloquer l'opération principale
            return None

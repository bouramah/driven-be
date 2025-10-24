from app.common.models import Page, Application, db
from app.common.utils.file_manager import FileManager

class PageService:
    def __init__(self):
        self.file_manager = FileManager(
            upload_folder='uploads/pages',
            allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'svg'}
        )
    
    def get_all_pages(self):
        return Page.query.all()
    
    def get_page_by_id(self, page_id):
        return Page.query.get(page_id)
    
    def create_page(self, page_data, icon_file=None):
        # Vérifier si l'application existe si app_id est fourni
        if 'app_id' in page_data and page_data['app_id']:
            application = Application.query.get(page_data['app_id'])
            if not application:
                raise ValueError(f"L'application avec l'ID {page_data['app_id']} n'existe pas")
            
            # Vérifier si une page avec le même nom existe déjà dans cette application
            existing_page = Page.query.filter_by(
                nom=page_data.get('nom'),
                app_id=page_data['app_id']
            ).first()
            if existing_page:
                raise ValueError(f"Une page avec le nom '{page_data.get('nom')}' existe déjà dans cette application")

        if icon_file:
            icon_path = self.file_manager.save_file(icon_file)
            if icon_path:
                page_data['icon'] = icon_path
                
        page = Page(**page_data)
        db.session.add(page)
        db.session.commit()
        return page
    
    def update_page(self, page_id, page_data, icon_file=None):
        page = self.get_page_by_id(page_id)
        if not page:
            return None
        
        # Vérifier si l'application existe si app_id est modifié
        if 'app_id' in page_data and page_data['app_id'] and page_data['app_id'] != page.app_id:
            application = Application.query.get(page_data['app_id'])
            if not application:
                raise ValueError(f"L'application avec l'ID {page_data['app_id']} n'existe pas")
        
        # Vérifier si le nom est modifié et s'il existe déjà dans l'application
        app_id = page_data.get('app_id', page.app_id)
        if 'nom' in page_data and (page_data['nom'] != page.nom or app_id != page.app_id):
            existing_page = Page.query.filter(
                Page.nom == page_data['nom'],
                Page.app_id == app_id,
                Page.page_id != page_id
            ).first()
            if existing_page:
                raise ValueError(f"Une page avec le nom '{page_data['nom']}' existe déjà dans cette application")
        
        if icon_file:
            # Supprimer l'ancienne icône si elle existe
            if page.icon:
                self.file_manager.delete_file(page.icon)
            
            # Sauvegarder la nouvelle icône
            icon_path = self.file_manager.save_file(icon_file)
            if icon_path:
                page_data['icon'] = icon_path
            
        for key, value in page_data.items():
            setattr(page, key, value)
            
        db.session.commit()
        return page
    
    def delete_page(self, page_id):
        page = self.get_page_by_id(page_id)
        if page:
            # Supprimer l'icône si elle existe
            if hasattr(page, 'icon') and page.icon:
                self.file_manager.delete_file(page.icon)
                
            db.session.delete(page)
            db.session.commit()
            return True
        return False
    
    def get_pages_by_application(self, app_id):
        return Page.query.filter_by(app_id=app_id).all()
    
    def add_pages_to_application(self, app_id, page_ids):
        """Ajoute plusieurs pages à une application"""
        application = Application.query.get(app_id)
        if not application:
            return False
        
        pages = Page.query.filter(Page.page_id.in_(page_ids)).all()
        for page in pages:
            page.app_id = app_id
        
        db.session.commit()
        return True
    
    def remove_pages_from_application(self, app_id, page_ids):
        """Retire plusieurs pages d'une application"""
        pages = Page.query.filter(
            Page.app_id == app_id,
            Page.page_id.in_(page_ids)
        ).all()
        
        if not pages:
            return False
        
        for page in pages:
            page.app_id = None
        
        db.session.commit()
        return True 
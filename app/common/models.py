from datetime import datetime
from app import db

class Application(db.Model):
    __tablename__ = 'application'
    
    app_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    app_color = db.Column(db.String(20), nullable=False)
    app_icon = db.Column(db.String(100), nullable=True)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    pages = db.relationship('Page', back_populates='application')
    roles = db.relationship('Role', back_populates='application')
    utilisateur_roles = db.relationship('UtilisateurRole', back_populates='application')
    utilisateurs = db.relationship('Utilisateur', secondary='utilisateur_role', viewonly=True, overlaps="utilisateur_roles")

class Page(db.Model):
    __tablename__ = 'page'
    
    page_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lien = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=True)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    app_id = db.Column(db.Integer, db.ForeignKey('application.app_id'), nullable=True)
    
    # Relation avec back_populates
    application = db.relationship('Application', back_populates='pages')

class FonctionAPI(db.Model):
    __tablename__ = 'fonction_api'
    
    fonction_id = db.Column(db.Integer, primary_key=True)
    nom_fonction = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('application.app_id'), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    application = db.relationship('Application', backref=db.backref('fonctions_api', lazy=True))
    fonction_permissions = db.relationship('FonctionPermission', back_populates='fonction', cascade='all, delete-orphan')

class FonctionPermission(db.Model):
    __tablename__ = 'fonction_permission'
    
    fp_id = db.Column(db.Integer, primary_key=True)
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonction_api.fonction_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    fonction = db.relationship('FonctionAPI', back_populates='fonction_permissions')
    permission = db.relationship('Permission', back_populates='fonction_permissions')

class Permission(db.Model):
    __tablename__ = 'permission'
    
    permission_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    fonction_permissions = db.relationship('FonctionPermission', back_populates='permission', cascade='all, delete-orphan')

class PermissionPage(db.Model):
    __tablename__ = 'permission_page'
    
    pp_id = db.Column(db.Integer, primary_key=True)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    page_id = db.Column(db.Integer, db.ForeignKey('page.page_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), nullable=False)

class Role(db.Model):
    __tablename__ = 'role'
    
    role_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('application.app_id'), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    application = db.relationship('Application', back_populates='roles')
    utilisateur_roles = db.relationship('UtilisateurRole', back_populates='role', cascade='all, delete-orphan')
    utilisateurs = db.relationship('Utilisateur', secondary='utilisateur_role', viewonly=True, overlaps="utilisateur_roles")

class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    
    rp_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    role = db.relationship('Role', backref=db.backref('role_permissions', lazy=True))
    permission = db.relationship('Permission', backref=db.backref('role_permissions', lazy=True))

class Entite(db.Model):
    __tablename__ = 'entite'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class UtilisateurRole(db.Model):
    __tablename__ = 'utilisateur_role'
    
    ur_id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('application.app_id'), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations avec back_populates pour éviter les chevauchements
    utilisateur = db.relationship('Utilisateur', back_populates='utilisateur_roles')
    role = db.relationship('Role', back_populates='utilisateur_roles')
    application = db.relationship('Application', back_populates='utilisateur_roles')

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    statut = db.Column(db.String(20), nullable=False)
    date_expiration = db.Column(db.DateTime, nullable=True)
    profil = db.Column(db.String(50), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    id_entite = db.Column(db.Integer, db.ForeignKey('entite.id'), nullable=False)
        
    # Relations
    utilisateur_roles = db.relationship('UtilisateurRole', back_populates='utilisateur', cascade='all, delete-orphan')
    entite = db.relationship('Entite', backref='utilisateurs')    
    # Relations many-to-many avec overlaps pour éviter les avertissements
    roles = db.relationship('Role', secondary='utilisateur_role', viewonly=True, overlaps="utilisateur_roles")
    
    @property
    def applications(self):
        """Récupère les applications auxquelles l'utilisateur a accès via ses rôles"""
        # Utiliser un set pour éviter les doublons
        return list({ur.application for ur in self.utilisateur_roles})
    
    def has_permission_for_fonction(self, app_id, nom_fonction):
        """
        Vérifie si l'utilisateur a la permission d'accéder à une fonction API spécifique.
        
        Args:
            app_id (int): ID de l'application
            nom_fonction (str): Nom de la fonction API
            
        Returns:
            bool: True si l'utilisateur a la permission, False sinon
        """
        # 1. Récupérer tous les rôles de l'utilisateur pour cette application
        user_roles = UtilisateurRole.query.filter_by(
            id_utilisateur=self.id_utilisateur,
            app_id=app_id
        ).all()
        
        if not user_roles:
            return False
        
        role_ids = [ur.role_id for ur in user_roles]
        
        # 2. Trouver la fonction API correspondante dans la base de données
        fonction = FonctionAPI.query.filter(
            FonctionAPI.nom_fonction == nom_fonction,
            FonctionAPI.app_id == app_id
        ).first()
        
        if not fonction:
            return False
        
        # 3. Récupérer toutes les permissions associées à cette fonction
        fonction_permissions = FonctionPermission.query.filter_by(
            fonction_id=fonction.fonction_id
        ).all()
        
        # Si aucune permission n'est associée à cette fonction, permettre l'accès
        # à tous les utilisateurs qui ont au moins un rôle pour cette application
        if not fonction_permissions:
            return True
        
        permission_ids = [fp.permission_id for fp in fonction_permissions]
        
        # 4. Vérifier si l'un des rôles de l'utilisateur a une permission pour cette fonction
        role_permissions = RolePermission.query.filter(
            RolePermission.role_id.in_(role_ids),
            RolePermission.permission_id.in_(permission_ids)
        ).first()
        
        return role_permissions is not None

class Trace(db.Model):
    __tablename__ = 'trace'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    action = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text, nullable=True)
    code = db.Column(db.String(50), nullable=True)
    param = db.Column(db.Text, nullable=True)
    code_sql = db.Column(db.Text, nullable=True)
    end_point = db.Column(db.String(400), nullable=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    
    # Relations
    utilisateur = db.relationship('Utilisateur', backref='traces', lazy=True)

class BlackList(db.Model):
    __tablename__ = 'black_list'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    structure = db.Column(db.String(200), nullable=False)
    date_ajout = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Codification(db.Model):
    __tablename__ = 'codification'
    
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(200), nullable=False)
    param = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id_set = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    id_codification = db.Column(db.Integer, db.ForeignKey('codification.id'), nullable=False)
    
    # Ajouter les relations
    utilisateur = db.relationship('Utilisateur', backref='settings')
    codification = db.relationship('Codification', backref='settings')

class Objectif(db.Model):
    __tablename__ = 'objectif'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    periode = db.Column(db.String(100), nullable=False)
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.String(50), nullable=False, default='En cours')
    progression = db.Column(db.Float, nullable=False, default=0.0)
    valeur = db.Column(db.Float, nullable=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    creer_par = db.Column(db.Integer, nullable=False)
    modifier_par = db.Column(db.Integer, nullable=False)
    creer_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 
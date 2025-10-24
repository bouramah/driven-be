from datetime import datetime
from app import db

class TypeDemande(db.Model):
    __tablename__ = 'types_demande'
    
    id_type = db.Column(db.Integer, primary_key=True)
    nom_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    delai_en_jour = db.Column(db.Integer, nullable=True)
    creer_par = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    modifier_par = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    creer_a = db.Column(db.DateTime, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TypeDemande {self.nom_type}>"

    def to_dict(self):
        return {
            'id_type': self.id_type,
            'nom_type': self.nom_type,
            'description': self.description,
            'delai_en_jour': self.delai_en_jour,
            'creer_par': self.creer_par,
            'modifier_par': self.modifier_par,
            'creer_a': self.creer_a.isoformat(),
            'modifier_a': self.modifier_a.isoformat()
        }
    def to_dict2(self):
        return {
            'nom_type': self.nom_type,
            'description': self.description,
            'delai_en_jour': self.delai_en_jour
        }



class Demande(db.Model):
    __tablename__ = 'demande'
    
    id_demande = db.Column(db.Integer, primary_key=True)
    numero_demande = db.Column(db.String(100), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    contenu_sql = db.Column(db.Text, nullable=True)
    chemin_fichier = db.Column(db.String(255), nullable=True)
    statut = db.Column(db.String(50), nullable=False)
    niveau_priorite = db.Column(db.String(50), nullable=False)
    date_initiation = db.Column(db.DateTime, nullable=False)
    date_prise_en_charge = db.Column(db.DateTime, nullable=True)
    date_fin = db.Column(db.DateTime, nullable=True)
    id_utilisateur_demandeur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    id_traiteur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    id_type_demande = db.Column(db.Integer, db.ForeignKey('types_demande.id_type'), nullable=False)
    creer_par = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    modifier_par = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    creer_a = db.Column(db.DateTime, default=datetime.utcnow)
    modifier_a = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    utilisateur_demandeur = db.relationship('Utilisateur', foreign_keys=[id_utilisateur_demandeur], backref=db.backref('demandes_comme_demandeur', lazy=True))
    traiteur = db.relationship('Utilisateur', foreign_keys=[id_traiteur], backref=db.backref('demandes_comme_traiteur', lazy=True))
    type_demande = db.relationship('TypeDemande', backref=db.backref('demandes', lazy=True))

    def __repr__(self):
        return f"<Demande {self.numero_demande} - {self.statut}>"

    def to_dict(self):
        return {
            'id_demande': self.id_demande,
            'numero_demande': self.numero_demande,
            'nom': self.nom,
            'description': self.description,
            'contenu_sql': self.contenu_sql,
            'chemin_fichier': self.chemin_fichier,
            'statut': self.statut,
            'niveau_priorite': self.niveau_priorite,
            'date_initiation': self.date_initiation.isoformat(),
            'date_prise_en_charge': self.date_prise_en_charge.isoformat() if self.date_prise_en_charge else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'id_utilisateur_demandeur': self.id_utilisateur_demandeur,
            'id_traiteur': self.id_traiteur,
            'id_type_demande': self.id_type_demande,
            'creer_par': self.creer_par,
            'modifier_par': self.modifier_par,
            'creer_a': self.creer_a.isoformat(),
            'modifier_a': self.modifier_a.isoformat(),
            'utilisateur_demandeur_details': self.utilisateur_demandeur.to_dict2() if self.utilisateur_demandeur else None,
            'traiteur_details': self.traiteur.to_dict2() if self.traiteur else None,
            'type_demande_details': self.type_demande.to_dict2() if self.type_demande else None
        }
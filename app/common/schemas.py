from marshmallow import Schema, fields

class ApplicationSchema(Schema):
    app_id = fields.Int()
    nom = fields.Str()
    description = fields.Str()
    app_color = fields.Str()
    app_icon = fields.Str()
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)

class PageSchema(Schema):
    page_id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    description = fields.Str(required=True)
    lien = fields.Str(required=True)
    icon = fields.Str(required=False)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)
    app_id = fields.Int(required=True)

class PermissionSchema(Schema):
    permission_id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    description = fields.Str(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)

class PermissionPageSchema(Schema):
    pp_id = fields.Int(dump_only=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)
    page_id = fields.Int(required=True)
    permission_id = fields.Int(required=True)
    
class RolePermissionSchema(Schema):
    rp_id = fields.Int(dump_only=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)
    role_id = fields.Int(required=True)
    permission_id = fields.Int(required=True)
    permission = fields.Nested(PermissionSchema, dump_only=True)

class RoleSchema(Schema):
    role_id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    description = fields.Str(required=True)
    app_id = fields.Int(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)
    application = fields.Nested(ApplicationSchema, dump_only=True)
    permissions = fields.Method("get_permissions", dump_only=True)
    
    def get_permissions(self, obj):
        """Extraire uniquement les permissions du rôle"""
        permissions = []
        if hasattr(obj, 'role_permissions'):
            for rp in obj.role_permissions:
                if rp.permission:
                    permissions.append({
                        'permission_id': rp.permission.permission_id,
                        'nom': rp.permission.nom,
                        'description': rp.permission.description,
                        'creer_par': rp.permission.creer_par,
                        'modifier_par': rp.permission.modifier_par,
                        'creer_a': rp.permission.creer_a,
                        'modifier_a': rp.permission.modifier_a
                    })
        return permissions

class EntiteSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    code = fields.Str(required=True)
    email = fields.Str(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)

class UtilisateurRoleSchema(Schema):
    ur_id = fields.Int(dump_only=True)
    id_utilisateur = fields.Int(required=True)
    role_id = fields.Int(required=True)
    app_id = fields.Int(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)
    role = fields.Nested(RoleSchema, dump_only=True)
    application = fields.Nested(ApplicationSchema, dump_only=True)

class UtilisateurSchema(Schema):
    id_utilisateur = fields.Int(dump_only=True)
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    login = fields.Str(required=True)
    email = fields.Str(required=True)
    statut = fields.Str(required=True)
    date_expiration = fields.DateTime(required=False, allow_none=True)
    profil = fields.Str(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)
    id_entite = fields.Int(required=True)
    utilisateur_roles = fields.Nested(UtilisateurRoleSchema, many=True, dump_only=True)
    entite = fields.Nested(EntiteSchema, dump_only=True)
    applications = fields.Nested(ApplicationSchema, many=True)

class TraceSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.DateTime(dump_only=True)
    action = fields.Str(required=True)
    detail = fields.Str(required=False)
    code = fields.Str(required=False)
    param = fields.Str(required=False)
    code_sql = fields.Str(required=False)
    end_point = fields.Str(required=False)
    id_utilisateur = fields.Int(required=False)
    utilisateur = fields.Nested(UtilisateurSchema, dump_only=True)

class BlackListSchema(Schema):
    id = fields.Int(dump_only=True)
    numero = fields.Str(required=True)
    nom = fields.Str(required=True)
    structure = fields.Str(required=True)
    date_ajout = fields.DateTime(dump_only=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)

class CodificationSchema(Schema):
    id = fields.Int(dump_only=True)
    libelle = fields.Str(required=True)
    param = fields.Str(required=True)
    description = fields.Str(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True)

class SettingsSchema(Schema):
    id_set = fields.Int()
    id_utilisateur = fields.Int()
    id_codification = fields.Int()
    codification = fields.Nested(CodificationSchema)

class ObjectifSchema(Schema):
    id = fields.Int(dump_only=True)
    titre = fields.Str(required=True)
    description = fields.Str(required=True)
    type = fields.Str(required=True)
    periode = fields.Str(required=True)
    date_debut = fields.DateTime(required=True)
    date_fin = fields.DateTime(required=True)
    statut = fields.Str(required=False)
    progression = fields.Float(required=False)
    valeur = fields.Float(required=False)
    id_utilisateur = fields.Int(required=True)
    creer_par = fields.Int(required=True)
    modifier_par = fields.Int(required=True)
    creer_a = fields.DateTime(dump_only=True)
    modifier_a = fields.DateTime(dump_only=True) 

class FonctionAPISchema(Schema):
    fonction_id = fields.Int()
    nom_fonction = fields.Str()
    description = fields.Str()
    app_id = fields.Int()
    creer_par = fields.Int()
    modifier_par = fields.Int()
    creer_a = fields.DateTime()
    modifier_a = fields.DateTime()
    application = fields.Nested(ApplicationSchema)


#!/usr/bin/env python3
"""
Script pour créer une proposition de rôles basée sur l'analyse des permissions
"""

import sqlite3
from datetime import datetime

DB_PATH = '/Users/ibrahimadoutyoulare/Documents/Code Orange/Driven/driven-be/instance/app.db'

# Structure proposée des rôles avec leurs permissions
ROLES_PROPOSITION = {
    "Administrateur Système": {
        "description": "Accès complet à toutes les fonctionnalités du système. Peut gérer applications, utilisateurs, rôles, permissions, et toutes les ressources.",
        "permissions_patterns": [
            # Toutes les permissions
            "*"  # Toutes les permissions
        ]
    },
    "Administrateur Application": {
        "description": "Gère les applications, utilisateurs, rôles et permissions dans une ou plusieurs applications. Ne peut pas supprimer des applications.",
        "permissions_patterns": [
            # Applications (lecture et modification, pas suppression)
            "get_applications", "get_application", "get_my_applications",
            "create_application", "update_application",
            
            # Utilisateurs (tous)
            "create_utilisateur", "update_utilisateur", "delete_utilisateur",
            "get_utilisateur", "get_utilisateurs", "get_all_users",
            "search_utilisateurs", "assign_role", "remove_role", "clone_roles",
            "prolonger_utilisateur", "verifier_eligibilite",
            
            # Rôles (tous)
            "create_role", "update_role", "delete_role",
            "get_role", "get_roles", "get_roles_by_app", "get_role_permissions",
            "get_roles_with_permission",
            
            # Permissions (tous)
            "create_permission", "update_permission", "delete_permission",
            "get_permissions",
            
            # Fonctions API
            "get_fonctions", "get_fonction", "get_fonctions_by_app",
            "create_fonction", "update_fonction", "delete_fonction",
            "assign_permission", "assign_permissions", "remove_permissions",
            "get_fonction_permissions",
            
            # Pages
            "get_pages", "get_page", "get_pages_by_application",
            "create_page", "update_page", "delete_page",
            "create_permission_page", "delete_permission_page",
            "get_permission_pages", "get_permission_pages_by_page",
            
            # Entités
            "get_entites", "create_entite", "update_entite", "delete_entite",
            
            # Paramètres
            "get_settings", "get_setting", "get_settings_by_utilisateur",
            "create_setting", "update_setting", "delete_setting",
            
            # Traces (lecture)
            "get_traces", "get_trace", "get_traces_by_action",
            "get_traces_by_utilisateur", "get_traces_by_date_range",
            "search_traces"
        ]
    },
    "Gestionnaire Utilisateurs": {
        "description": "Gère les utilisateurs : création, modification, suppression, assignation de rôles. Accès en lecture aux rôles et entités.",
        "permissions_patterns": [
            # Utilisateurs
            "create_utilisateur", "update_utilisateur", "delete_utilisateur",
            "get_utilisateur", "get_utilisateurs", "get_all_users",
            "get_utilisateurs_by_entite", "get_utilisateurs_by_role",
            "get_utilisateurs_by_application", "search_utilisateurs",
            "assign_role", "remove_role", "clone_roles",
            "prolonger_utilisateur", "verifier_eligibilite",
            "get_utilisateur_roles", "get_utilisateur_by_login",
            "get_utilisateur_by_email", "get_available_users",
            
            # Rôles (lecture)
            "get_role", "get_roles", "get_roles_by_app", "get_role_permissions",
            
            # Entités (lecture)
            "get_entites",
            
            # Applications (lecture)
            "get_applications", "get_application", "get_my_applications"
        ]
    },
    "Gestionnaire Rôles et Permissions": {
        "description": "Gère les rôles, permissions et leurs associations avec les fonctions API et pages.",
        "permissions_patterns": [
            # Rôles
            "create_role", "update_role", "delete_role",
            "get_role", "get_roles", "get_roles_by_app", "get_role_permissions",
            "get_roles_with_permission",
            
            # Permissions
            "create_permission", "update_permission", "delete_permission",
            "get_permissions",
            
            # Fonctions API
            "get_fonctions", "get_fonction", "get_fonctions_by_app",
            "create_fonction", "update_fonction", "delete_fonction",
            "assign_permission", "assign_permissions", "remove_permissions",
            "get_fonction_permissions", "search_fonctions",
            
            # Pages
            "get_pages", "get_page", "get_pages_by_application",
            "create_page", "update_page", "delete_page",
            "create_permission_page", "delete_permission_page",
            "get_permission_pages", "get_permission_pages_by_page",
            
            # Utilisateurs (lecture)
            "get_utilisateur", "get_utilisateurs", "get_all_users",
            "get_utilisateur_roles", "get_utilisateurs_by_role",
            "get_roles_with_permission",
            
            # Applications (lecture)
            "get_applications", "get_application", "get_my_applications"
        ]
    },
    "Opérateur": {
        "description": "Accès en lecture seule à la plupart des ressources. Peut consulter les utilisateurs, rôles, applications, pages.",
        "permissions_patterns": [
            # Utilisateurs (lecture)
            "get_utilisateur", "get_utilisateurs", "get_all_users",
            "get_utilisateur_by_login", "get_utilisateur_by_email",
            "get_utilisateurs_by_entite", "get_utilisateurs_by_role",
            "get_utilisateurs_by_application",
            
            # Rôles (lecture)
            "get_role", "get_roles", "get_roles_by_app", "get_role_permissions",
            
            # Permissions (lecture)
            "get_permissions",
            
            # Applications (lecture)
            "get_applications", "get_application", "get_my_applications",
            
            # Fonctions API (lecture)
            "get_fonctions", "get_fonction", "get_fonctions_by_app",
            "get_fonction_permissions",
            
            # Pages (lecture)
            "get_pages", "get_page", "get_pages_by_application",
            "get_permission_pages", "get_permission_pages_by_page",
            
            # Entités (lecture)
            "get_entites",
            
            # Paramètres (lecture)
            "get_settings", "get_setting", "get_settings_by_utilisateur",
            
            # Objectifs (lecture)
            "get_objectifs", "get_objectif", "get_objectifs_by_periode",
            "get_objectifs_by_type", "get_objectifs_by_utilisateur",
            
            # Codifications (lecture)
            "get_codifications", "get_codification_by_param",
            
            # BlackList (lecture)
            "get_blacklists", "get_blacklist", "get_blacklist_by_number",
            "is_number_blacklisted"
        ]
    },
    "Gestionnaire Métier": {
        "description": "Gère les données métier : objectifs, codifications, blacklist. Peut créer, modifier et supprimer ces éléments.",
        "permissions_patterns": [
            # Objectifs
            "create_objectif", "update_objectif", "delete_objectif",
            "get_objectifs", "get_objectif", "get_objectifs_by_periode",
            "get_objectifs_by_type", "get_objectifs_by_utilisateur",
            "get_available_users",
            
            # Codifications
            "create_codification", "update_codification", "delete_codification",
            "get_codifications", "get_codification_by_param", "search_codifications",
            
            # BlackList
            "create_blacklist", "update_blacklist", "delete_blacklist",
            "get_blacklists", "get_blacklist", "get_blacklist_by_number",
            "is_number_blacklisted",
            
            # Utilisateurs (lecture pour assigner objectifs)
            "get_utilisateur", "get_utilisateurs", "get_available_users",
            
            # Applications (lecture)
            "get_applications", "get_application", "get_my_applications"
        ]
    },
    "Auditeur": {
        "description": "Accès aux traces et logs pour audit et surveillance. Peut consulter toutes les traces du système.",
        "permissions_patterns": [
            # Traces (tous)
            "get_traces", "get_trace", "get_traces_by_action",
            "get_traces_by_utilisateur", "get_traces_by_date_range",
            "search_traces",
            
            # Utilisateurs (lecture pour contexte)
            "get_utilisateur", "get_utilisateurs",
            
            # Applications (lecture)
            "get_applications", "get_application"
        ]
    },
    "Support Technique": {
        "description": "Gère les paramètres système et configurations. Accès en lecture aux ressources pour diagnostic.",
        "permissions_patterns": [
            # Paramètres
            "create_setting", "update_setting", "delete_setting",
            "get_settings", "get_setting", "get_settings_by_utilisateur",
            
            # Codifications (pour configuration)
            "get_codifications", "get_codification_by_param",
            "create_codification", "update_codification",
            
            # Traces (lecture pour diagnostic)
            "get_traces", "get_trace", "get_traces_by_action",
            "get_traces_by_utilisateur", "search_traces",
            
            # Applications (lecture)
            "get_applications", "get_application", "get_my_applications",
            
            # Fonctions API (lecture)
            "get_fonctions", "get_fonction", "get_fonctions_by_app"
        ]
    },
    "Consultant": {
        "description": "Accès en lecture seule aux données de consultation (objectifs, codifications, blacklist). Pas d'accès aux données sensibles.",
        "permissions_patterns": [
            # Objectifs (lecture)
            "get_objectifs", "get_objectif", "get_objectifs_by_periode",
            "get_objectifs_by_type", "get_objectifs_by_utilisateur",
            
            # Codifications (lecture)
            "get_codifications", "get_codification_by_param", "search_codifications",
            
            # BlackList (lecture)
            "get_blacklists", "get_blacklist", "get_blacklist_by_number",
            "is_number_blacklisted",
            
            # Applications (lecture)
            "get_applications", "get_application", "get_my_applications"
        ]
    }
}

def get_permission_ids_by_pattern(pattern, all_permissions):
    """Trouve les IDs de permissions correspondant à un pattern"""
    matching_ids = []
    pattern_lower = pattern.lower()
    
    for perm in all_permissions:
        perm_name_lower = perm['nom'].lower()
        # Pour "*", on prend toutes les permissions
        if pattern == "*":
            matching_ids.append(perm['permission_id'])
        # Sinon on cherche si le pattern est dans le nom de permission
        elif pattern_lower in perm_name_lower or perm_name_lower.endswith(pattern_lower):
            matching_ids.append(perm['permission_id'])
    
    return matching_ids

def generate_roles_proposition():
    """Génère la proposition de rôles avec leurs permissions"""
    
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    # Récupérer toutes les permissions
    cur.execute('SELECT permission_id, nom, description FROM permission ORDER BY permission_id')
    all_permissions = cur.fetchall()
    
    # Récupérer l'app_id de l'application Administration
    cur.execute('SELECT app_id FROM application WHERE nom = ?', ('Administration',))
    app_row = cur.fetchone()
    admin_app_id = app_row['app_id'] if app_row else 1
    
    print("=" * 80)
    print("PROPOSITION DE RÔLES POUR L'APPLICATION ADMINISTRATION")
    print("=" * 80)
    print(f"\nApplication ID: {admin_app_id}")
    print(f"Nombre total de permissions disponibles: {len(all_permissions)}\n")
    
    roles_with_permissions = {}
    
    for role_name, role_info in ROLES_PROPOSITION.items():
        print(f"\n{'=' * 80}")
        print(f"RÔLE: {role_name}")
        print(f"{'=' * 80}")
        print(f"Description: {role_info['description']}")
        print(f"\nPermissions associées:")
        
        permission_ids = set()
        for pattern in role_info['permissions_patterns']:
            pattern_ids = get_permission_ids_by_pattern(pattern, all_permissions)
            permission_ids.update(pattern_ids)
            
            # Afficher quelques exemples
            if pattern != "*" and len(pattern_ids) > 0:
                example_perms = [p for p in all_permissions if p['permission_id'] in pattern_ids[:3]]
                for perm in example_perms:
                    print(f"  ✓ {perm['nom']}")
                if len(pattern_ids) > 3:
                    print(f"  ... et {len(pattern_ids) - 3} autres permissions pour '{pattern}'")
            elif pattern == "*":
                print(f"  ✓ TOUTES LES PERMISSIONS ({len(all_permissions)} permissions)")

        # Enrichissement par dépendances fonctionnelles
        # Si le rôle peut créer/modifier/supprimer des objectifs, ajouter les lectures nécessaires
        def has_perm_name_contains(substrs):
            substrs_lower = [s.lower() for s in substrs]
            for pid in permission_ids:
                perm = next((p for p in all_permissions if p['permission_id'] == pid), None)
                if perm and any(s in perm['nom'].lower() for s in substrs_lower):
                    return True
            return False

        # Dépendances pour gestion des objectifs -> nécessite lecture utilisateurs et applications
        if has_perm_name_contains(["create_objectif", "update_objectif", "delete_objectif"]):
            deps_patterns = [
                # Utilisateurs (lecture et listes nécessaires)
                "get_utilisateurs", "get_all_users", "get_available_users",
                # Applications (lecture)
                "get_applications", "get_application", "get_my_applications"
            ]
            for dp in deps_patterns:
                permission_ids.update(get_permission_ids_by_pattern(dp, all_permissions))

        # Dépendances pour gestion des pages -> lecture applications
        if has_perm_name_contains(["create_page", "update_page", "delete_page"]):
            deps_patterns = ["get_applications", "get_application", "get_pages_by_application"]
            for dp in deps_patterns:
                permission_ids.update(get_permission_ids_by_pattern(dp, all_permissions))

        # Dépendances pour gestion des rôles/permissions -> utilisateurs (lecture basique)
        if has_perm_name_contains(["create_role", "update_role", "delete_role", "assign_permission", "assign_permissions", "remove_permissions"]):
            deps_patterns = ["get_utilisateurs", "get_all_users", "get_utilisateur_roles"]
            for dp in deps_patterns:
                permission_ids.update(get_permission_ids_by_pattern(dp, all_permissions))
        
        roles_with_permissions[role_name] = {
            'description': role_info['description'],
            'permission_ids': sorted(list(permission_ids)),
            'count': len(permission_ids)
        }
        
        print(f"\nTotal: {len(permission_ids)} permissions")
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    for role_name, data in roles_with_permissions.items():
        print(f"{role_name}: {data['count']} permissions")
    
    return roles_with_permissions, admin_app_id

if __name__ == "__main__":
    roles_with_permissions, app_id = generate_roles_proposition()

    # Insertion optionnelle en base
    import argparse
    parser = argparse.ArgumentParser(description="Proposer et éventuellement créer les rôles dans la base")
    parser.add_argument('--apply', action='store_true', help='Créer/mettre à jour les rôles et leurs permissions dans la base')
    parser.add_argument('--app-id', type=int, default=None, help="Forcer l'app_id pour les rôles (défaut: Administration)")
    parser.add_argument('--actor-id', type=int, default=1, help='ID utilisateur pour creer_par/modifier_par (défaut: 1)')
    args, unknown = parser.parse_known_args()

    print("\n" + "=" * 80)
    print("STRUCTURE JSON POUR CRÉATION")
    print("=" * 80)
    print("\nVous pouvez utiliser cette structure pour créer les rôles dans la base de données.")
    print(f"\nApp ID à utiliser: {args.app_id or app_id}")

    if args.apply:
        target_app_id = args.app_id or app_id
        CREER_PAR = args.actor_id
        MODIFIER_PAR = args.actor_id

        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # Charger toutes les permissions (id -> nom)
        cur.execute('SELECT permission_id, nom FROM permission')
        perm_rows = cur.fetchall()
        permission_id_set = {r['permission_id'] for r in perm_rows}

        created_roles = 0
        updated_roles = 0
        created_links = 0

        for role_name, data in roles_with_permissions.items():
            description = data['description']
            permission_ids = [pid for pid in data['permission_ids'] if pid in permission_id_set]

            # Vérifier si le rôle existe (par nom + app_id)
            cur.execute('SELECT role_id FROM role WHERE nom = ? AND app_id = ?', (role_name, target_app_id))
            row = cur.fetchone()
            if row is None:
                cur.execute(
                    'INSERT INTO role (nom, description, creer_par, modifier_par, creer_a, modifier_a, app_id) VALUES (?,?,?,?,?,?,?)',
                    (role_name, description, CREER_PAR, MODIFIER_PAR, now, now, target_app_id)
                )
                role_id = cur.lastrowid
                created_roles += 1
            else:
                role_id = row['role_id']
                # Mettre éventuellement à jour la description
                cur.execute('UPDATE role SET description = ?, modifier_par = ?, modifier_a = ? WHERE role_id = ?',
                            (description, MODIFIER_PAR, now, role_id))
                updated_roles += 1

            # Créer les liaisons role_permission si non existantes
            for pid in permission_ids:
                cur.execute('SELECT 1 FROM role_permission WHERE role_id = ? AND permission_id = ?', (role_id, pid))
                if cur.fetchone() is None:
                    cur.execute(
                        'INSERT INTO role_permission (creer_par, modifier_par, creer_a, modifier_a, role_id, permission_id) VALUES (?,?,?,?,?,?)',
                        (CREER_PAR, MODIFIER_PAR, now, now, role_id, pid)
                    )
                    created_links += 1

        con.commit()
        print("\nApplication des rôles terminée:")
        print(f" - Rôles créés: {created_roles}")
        print(f" - Rôles mis à jour: {updated_roles}")
        print(f" - Liaisons role_permission créées: {created_links}")

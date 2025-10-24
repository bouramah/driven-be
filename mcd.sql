#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: Type_Demande
#------------------------------------------------------------

CREATE TABLE Type_Demande(
        ID_Type       Int  Auto_increment  NOT NULL ,
        Nom_Type      Varchar (300) NOT NULL ,
        Description   Text NOT NULL ,
        Delai_En_Jour Int NOT NULL ,
        creer_par     Int NOT NULL ,
        modifier_par  Int NOT NULL ,
        creer_a       TimeStamp NOT NULL ,
        modifier_a    TimeStamp NOT NULL
	,CONSTRAINT Type_Demande_PK PRIMARY KEY (ID_Type)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Black_list
#------------------------------------------------------------

CREATE TABLE Black_list(
        Id           Int  Auto_increment  NOT NULL ,
        Numero       Varchar (20) NOT NULL ,
        Nom          Varchar (200) NOT NULL ,
        Structure    Varchar (200) NOT NULL ,
        Date_ajout   TimeStamp NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL
	,CONSTRAINT Black_list_PK PRIMARY KEY (Id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Application
#------------------------------------------------------------

CREATE TABLE Application(
        App_id       Int  Auto_increment  NOT NULL ,
        Nom          Varchar (300) NOT NULL ,
        Description  Text NOT NULL ,
        App_color    Varchar (20) NOT NULL ,
        App_icon     Varchar (100) NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL
	,CONSTRAINT Application_PK PRIMARY KEY (App_id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Role
#------------------------------------------------------------

CREATE TABLE Role(
        Role_id      Int  Auto_increment  NOT NULL ,
        Nom          Varchar (300) NOT NULL ,
        Description  Text NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL
	,CONSTRAINT Role_PK PRIMARY KEY (Role_id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Page
#------------------------------------------------------------

CREATE TABLE Page(
        Page_id      Int  Auto_increment  NOT NULL ,
        Nom          Varchar (300) NOT NULL ,
        Description  Text NOT NULL ,
        Lien         Varchar (300) NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL ,
        App_id       Int NOT NULL
	,CONSTRAINT Page_PK PRIMARY KEY (Page_id)

	,CONSTRAINT Page_Application_FK FOREIGN KEY (App_id) REFERENCES Application(App_id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Permission
#------------------------------------------------------------

CREATE TABLE Permission(
        Permission_id Int  Auto_increment  NOT NULL ,
        Nom           Varchar (300) NOT NULL ,
        Description   Text NOT NULL ,
        creer_par     Int NOT NULL ,
        modifier_par  Int NOT NULL ,
        creer_a       TimeStamp NOT NULL ,
        modifier_a    TimeStamp NOT NULL
	,CONSTRAINT Permission_PK PRIMARY KEY (Permission_id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Permission_Page
#------------------------------------------------------------

CREATE TABLE Permission_Page(
        Pp_id         Int  Auto_increment  NOT NULL ,
        creer_par     Int NOT NULL ,
        modifier_par  Int NOT NULL ,
        creer_a       TimeStamp NOT NULL ,
        modifier_a    TimeStamp NOT NULL ,
        Page_id       Int NOT NULL ,
        Permission_id Int NOT NULL
	,CONSTRAINT Permission_Page_PK PRIMARY KEY (Pp_id)

	,CONSTRAINT Permission_Page_Page_FK FOREIGN KEY (Page_id) REFERENCES Page(Page_id)
	,CONSTRAINT Permission_Page_Permission0_FK FOREIGN KEY (Permission_id) REFERENCES Permission(Permission_id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Rôle_Permission
#------------------------------------------------------------

CREATE TABLE Role_Permission(
        Rp_id        Int  Auto_increment  NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL ,
        Role_id      Int NOT NULL ,
        Pp_id        Int NOT NULL
	,CONSTRAINT Role_Permission_PK PRIMARY KEY (Rp_id)

	,CONSTRAINT Role_Permission_Role_FK FOREIGN KEY (Role_id) REFERENCES Role(Role_id)
	,CONSTRAINT Role_Permission_Permission_Page0_FK FOREIGN KEY (Pp_id) REFERENCES Permission_Page(Pp_id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Entite
#------------------------------------------------------------

CREATE TABLE Entite(
        Id           Int  Auto_increment  NOT NULL ,
        Nom          Varchar (200) NOT NULL ,
        Code         Varchar (10) NOT NULL ,
        Email        Varchar (300) NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL
	,CONSTRAINT Entite_PK PRIMARY KEY (Id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Utilisateur
#------------------------------------------------------------

CREATE TABLE Utilisateur(
        ID_Utilisateur  Int  Auto_increment  NOT NULL ,
        Nom             Varchar (50) NOT NULL ,
        Prenom          Varchar (200) NOT NULL ,
        Login           Varchar (50) NOT NULL ,
        Email           Varchar (300) NOT NULL ,
        Statut          Varchar (50) NOT NULL ,
        Date_Expiration TimeStamp NOT NULL ,
        Profil          Varchar (50) NOT NULL ,
        creer_par       Int NOT NULL ,
        modifier_par    Int NOT NULL ,
        creer_a         TimeStamp NOT NULL ,
        modifier_a      TimeStamp NOT NULL ,
        Role_id         Int NOT NULL ,
        Id              Int NOT NULL
	,CONSTRAINT Utilisateur_PK PRIMARY KEY (ID_Utilisateur)

	,CONSTRAINT Utilisateur_Role_FK FOREIGN KEY (Role_id) REFERENCES Role(Role_id)
	,CONSTRAINT Utilisateur_Entite0_FK FOREIGN KEY (Id) REFERENCES Entite(Id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Trace
#------------------------------------------------------------

CREATE TABLE Trace(
        Id             Int  Auto_increment  NOT NULL ,
        Date           TimeStamp NOT NULL ,
        Action         Varchar (100) NOT NULL ,
        Detail         Text NOT NULL ,
        Code           Varchar (50) NOT NULL ,
        Param          Text NOT NULL ,
        Code_sql       Text NOT NULL ,
        End_point      Varchar (400) NOT NULL ,
        ID_Utilisateur Int NOT NULL
	,CONSTRAINT Trace_PK PRIMARY KEY (Id)

	,CONSTRAINT Trace_Utilisateur_FK FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Objectif
#------------------------------------------------------------

CREATE TABLE Objectif(
        Id             Int  Auto_increment  NOT NULL ,
        Libelle        Varchar (400) NOT NULL ,
        Periode        Float NOT NULL ,
        Valeur         Float NOT NULL ,
        Type           Varchar (20) NOT NULL COMMENT "Pourcentage ou nombre"  ,
        creer_par      Int NOT NULL ,
        modifier_par   Int NOT NULL ,
        creer_a        TimeStamp NOT NULL ,
        modifier_a     TimeStamp NOT NULL ,
        ID_Utilisateur Int NOT NULL
	,CONSTRAINT Objectif_PK PRIMARY KEY (Id)

	,CONSTRAINT Objectif_Utilisateur_FK FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Demande
#------------------------------------------------------------

CREATE TABLE Demande(
        ID_Demande             Int  Auto_increment  NOT NULL ,
        Numero_Demande         Varchar (50) NOT NULL ,
        Nom                    Varchar (200) NOT NULL ,
        Description            Text NOT NULL ,
        Contenu_SQL            Text NOT NULL ,
        Chemin_fichier         Varchar (200) NOT NULL ,
        Statut                 Varchar (50) NOT NULL COMMENT "ENUM('Initié', 'Pris en charge', 'Terminé')"  ,
        Niveau_priorite        Varchar (50) NOT NULL COMMENT "ENUM('Normal', 'Elevé', 'Tres Elevé')"  ,
        Date_initiation        TimeStamp NOT NULL ,
        Date_prise_en_charge   TimeStamp NOT NULL ,
        Date_fin               TimeStamp NOT NULL ,
        Scan_demande           Varchar (300) NOT NULL ,
        creer_par              Int NOT NULL ,
        modifier_par           Int NOT NULL ,
        creer_a                TimeStamp NOT NULL ,
        modifier_a             TimeStamp NOT NULL ,
        ID_Utilisateur         Int NOT NULL ,
        ID_Type                Int NOT NULL ,
        ID_Utilisateur_Traiter Int ,
        Id                     Int NOT NULL
	,CONSTRAINT Demande_PK PRIMARY KEY (ID_Demande)

	,CONSTRAINT Demande_Utilisateur_FK FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur)
	,CONSTRAINT Demande_Type_Demande0_FK FOREIGN KEY (ID_Type) REFERENCES Type_Demande(ID_Type)
	,CONSTRAINT Demande_Utilisateur1_FK FOREIGN KEY (ID_Utilisateur_Traiter) REFERENCES Utilisateur(ID_Utilisateur)
	,CONSTRAINT Demande_Entite2_FK FOREIGN KEY (Id) REFERENCES Entite(Id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Codification
#------------------------------------------------------------

CREATE TABLE Codification(
        Id           Int  Auto_increment  NOT NULL ,
        Libelle      Varchar (200) NOT NULL ,
        Param        Varchar (200) NOT NULL ,
        Description  Varchar (200) NOT NULL ,
        creer_par    Int NOT NULL ,
        modifier_par Int NOT NULL ,
        creer_a      TimeStamp NOT NULL ,
        modifier_a   TimeStamp NOT NULL
	,CONSTRAINT Codification_PK PRIMARY KEY (Id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Settings
#------------------------------------------------------------

CREATE TABLE Settings(
        Id_set         Int  Auto_increment  NOT NULL ,
        ID_Utilisateur Int NOT NULL ,
        Id             Int NOT NULL
	,CONSTRAINT Settings_PK PRIMARY KEY (Id_set)

	,CONSTRAINT Settings_Utilisateur_FK FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur)
	,CONSTRAINT Settings_Codification0_FK FOREIGN KEY (Id) REFERENCES Codification(Id)
)ENGINE=InnoDB;


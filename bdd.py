from sqlalchemy import MetaData,Column,Integer,Numeric,String,Date,Table,ForeignKey,Boolean,create_engine
import sqlite3


engine = create_engine('sqlite:///restaurant.db', echo = True)

metadata = MetaData()

restaurant_table = Table(
    "restaurant",
    metadata,
    Column("code_postal", Integer, primary_key=True),
    Column("espace_enfant", Boolean, unique=False, default=True),
    Column("parking", Boolean, unique=False, default=True),
    Column("borne_service_rapide",Boolean, unique=False, default=True),
    Column("acces_handicap",Boolean, unique=False, default=True),
    Column("departement", Integer, nullable=False),
    Column("Pays",ForeignKey("carte.pays"),nullable=False)
)
personnel_table = Table(
    "personnel",
    metadata,
    Column("personne_id",Integer,primary_key=True),
    Column("code_postal",ForeignKey("restaurant.code_postal"),nullable=False),
    Column("metier",String(35),nullable=False),
    Column("salaire",Numeric,nullable=False),
    Column("note",Integer,nullable=False),
    Column("experience",Integer,nullable=False),
    Column("manager", Integer,nullable=False)
)
carte_table = Table(
    "carte",
    metadata,
    Column("pays",String(35), primary_key=True),
    Column("produit_id", ForeignKey("produit.produit_id"), nullable=False)
)
produit_table = Table(    
    "produit",    
    metadata,    
    Column("produit_id", Integer, primary_key=True),
    Column("produit_nom", String(135), nullable=True),
    Column("prix",Integer,nullable=False)
)
commande_table = Table(    
    "commande",    
    metadata,    
    Column("commande_id", Integer, primary_key=True),
    Column("personne_id", ForeignKey("personnel.personne_id"), nullable=False),
    Column("pays", ForeignKey("carte.pays"),nullable=False),    
    Column("date", Date,nullable=False),
    Column("code_postal", ForeignKey("restaurant.code_postal"),nullable=False)
)
pc_table = Table(
    "pc",
    metadata,
    Column("pc_id",Integer,primary_key=True),
    Column("produit_id",ForeignKey("produit.produit_id"),nullable=False),
    Column("commande_id",ForeignKey("commande.commande_id"),nullable=False),
    Column("quantite",Integer,nullable=False)
)
ingredient_table = Table(
    "ingredient",
    metadata,
    Column("ingredient_id",Integer,primary_key=True),
    Column("ingredient_nom",String(35),nullable=False),
    Column("prix",Numeric,nullable=False)
)
recette_table = Table(
    "recette",
    metadata,
    Column("recette_id",Integer,primary_key= True),
    Column("produit_id",ForeignKey("produit.produit_id"),nullable=False),
    Column("ingredient_id",ForeignKey("ingredient.ingredient_id"),nullable=False),
    Column("quantité",Numeric,nullable=False)
)

stock_table = Table(
    "stock",
    metadata,
    Column("code_postal",ForeignKey("restaurant.code_postal"),nullable=False),
    Column("ingredient_id",ForeignKey("ingredient.ingredient_id"),nullable=False),
    Column("stock",Numeric,nullable=False)
)

historique_table = Table(
    "historique",
    metadata,
    Column("personne_id",ForeignKey("personnel.personne_id"),nullable=False),
    Column("date",Date,nullable=False),
    Column("Salaire",Numeric,nullable=False)
)
# Start transaction to commit DDL to postgres database

metadata.create_all(engine)    # Log the tables as they are created

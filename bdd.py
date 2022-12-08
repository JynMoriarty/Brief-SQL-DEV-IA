from sqlalchemy import MetaData,Column,Integer,Numeric,String,Date,Table,ForeignKey,create_engine
import sqlite3


engine = create_engine('sqlite:///restaurant.db', echo = True)

metadata = MetaData()

code_postal = Table(
    "code_postal",
    metadata,
    Column("code_postal",Integer, primary_key=True,autoincrement = False)
)

restaurant_table = Table(
    "restaurant",
    metadata,
    Column("restaurant_id",Integer,primary_key=True),
    Column("code_postal", Integer, ForeignKey("code_postal.code_postal")),
    Column("espace_enfant", Integer, unique=False, default=True),
    Column("parking", Integer, unique=False, default=True),
    Column("borne_service_rapide",Integer, unique=False, default=True),
    Column("acces_handicap",Integer, unique=False, default=True),
    Column("nombre_place",Integer,nullable=False),
    Column("departement", Integer, nullable=False),
    Column("pays_nom",ForeignKey("pays.pays_nom"),nullable=False)
)
personnel_table = Table(
    "personnel",
    metadata,
    Column("personne_id",Integer,primary_key=True),
    Column("code_postal",ForeignKey("code_postal.code_postal"),nullable=False),
    Column("restaurant_id",ForeignKey("restaurant.restaurant_id"),nullable=False),
    Column("metier",String(60),nullable=False),
    Column("salaire",Numeric,nullable=False),
    Column("nom",String(60),nullable= False),
    Column("adresse",String,nullable=False),
    Column("note",Integer,nullable=False),
    Column("experience",Integer,nullable=False),
    Column("manager", String(60))
)
pays_table = Table(
    "pays",
    metadata,
    Column("pays_id",Integer, primary_key=True),
    Column("pays_nom",String(70),nullable= False)
)
carte_table = Table(
    "carte",
    metadata,
    Column("pays_nom",ForeignKey("pays.pays_nom"),nullable= False),
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
    Column("restaurant_id",ForeignKey("restaurant.restaurant_id"),nullable=False),
    Column("pays_nom", ForeignKey("pays.pays_nom"),nullable=False),    
    Column("date", Date,nullable=False),
    Column("code_postal", ForeignKey("code_postal.code_postal"),nullable=False)
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
    Column("restaurant_id",ForeignKey("restaurant.restaurant_id"),nullable=False),
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

with engine.begin() as conn:
    metadata.create_all(conn)

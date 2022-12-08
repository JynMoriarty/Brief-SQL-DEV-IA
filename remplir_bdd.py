from sqlalchemy import MetaData,create_engine,select
from faker import Faker
from faker_food import FoodProvider
import sys
import datetime
from random import randint,uniform,choice
from ast import literal_eval

engine = create_engine('sqlite:///restaurant.db')

metadata = MetaData()

faker = Faker()
faker.add_provider(FoodProvider)

with engine.connect() as conn:
    metadata.reflect(conn)

produit = metadata.tables["produit"]
restaurant = metadata.tables["restaurant"]
carte=metadata.tables["carte"]
commande = metadata.tables["commande"]
pc = metadata.tables["pc"]
recette = metadata.tables["recette"]
ingredient = metadata.tables["ingredient"]
personnel = metadata.tables["personnel"]
stock = metadata.tables["stock"]
historique =metadata.tables["historique"]
pays = metadata.tables["pays"]

my_file = open("produit.txt", "r")
content = my_file.read()
produit_list = content.split(",")
my_file.close()

with engine.begin() as conn:
    for object in produit_list:
        insert_stmt= produit.insert().values(
        produit_nom = object,
        prix = round(uniform(1.00,12.00),2))
        conn.execute(insert_stmt)
with engine.begin() as conn:
   for _ in range(40):
        insert_stmt= ingredient.insert().values(
        ingredient_nom = faker.unique.ingredient(),
        prix = round(uniform(0.10,1.00),2))
        conn.execute(insert_stmt)

with engine.begin() as conn:
    for _ in range(26):
        insert_stmt = pays.insert().values(
        pays_nom = faker.unique.country()
        )
        conn.execute(insert_stmt)

with engine.begin() as conn :
    pa = conn.execute(select([pays.c.pays_nom])).fetchall()
print(pa)

for _ in range(26):                 #je boucle sur une range de 26 
    number = choice(range(20,30))   #je stock au préalable le nombre d'items ou de menus à ajouter à ma carte et le pays choisi
    random_pays = choice(pa)[0]
    with engine.begin() as conn:
        for _ in range(number):
            insert_stmt= carte.insert().values(  #pour un pays je choisis les produits de la carte 
            pays_nom = random_pays,
            produit_id = choice(range(1,271)))
            conn.execute(insert_stmt)
        
        
# with engine.begin() as conn:
#     for _ in range(100):
#         insert_stmt= restaurant.insert().values(
#         espace_enfant = faker.boolean(),
#         acces_handicap = faker.boolean(),
#         parking = faker.boolean(),
#         nombre_place = randint(20,100),
#         borne_service_rapide = faker.boolean()
#     )
#     conn.execute(insert_stmt)

# with engine.begin() as conn:
#     for _ in 100 :

#         insert_stmt= restaurant.insert().values(
#         metier = "directeur",
#         salaire= 10000,
#         note = 0,
#         experience = 0,
#         adresse = faker.adress.streetAdress(),
#         manager = faker.name()
        
#     )
#     conn.execute(insert_stmt)













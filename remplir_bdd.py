from sqlalchemy import MetaData,create_engine,select
from faker import Faker
from faker_food import FoodProvider
from random import randint,uniform,choice
from random import randrange
from datetime import timedelta
from datetime import datetime


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('1/1/2022 1:30 ', '%m/%d/%Y %I:%M ')
d2 = datetime.strptime('1/1/2023 4:50 ', '%m/%d/%Y %I:%M ')


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
code_postal = metadata.tables["code_postal"]

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


number_list1 = [i for i in range(50000,99999)]

           
with engine.begin() as conn:
    for _ in range(49999):
        n = choice(number_list1)
        number_list1.remove(n)
        insert_stmt = code_postal.insert().values(
            code_postal = n
        )
        conn.execute(insert_stmt)



for _ in range(26):                 #je boucle sur une range de 26 
    number = choice(range(20,30))   #je stock au préalable le nombre d'items ou de menus à ajouter à ma carte et le pays choisi
    random_pays = choice(pa)[0]
    number_produit = [i for i in range(270)]

    with engine.begin() as conn:
        for _ in range(number):
            n = choice(number_produit)
            number_produit.remove(n)
            insert_stmt= carte.insert().values(  #pour un pays je choisis les produits de la carte 
            pays_nom = random_pays,
            produit_id = choice(range(1,271)))
            conn.execute(insert_stmt)

for value in pa:
    random_pays = value[0]
    number_list = [i for i in range(50000,99999)]
    with engine.begin() as conn:
        for _ in range(1000):
           
            n = choice(number_list)
            number_list.remove(n)
            number = str(n)
            dep = int(number[:2])
            insert_stmt= restaurant.insert().values(
            code_postal = n,
            espace_enfant = randint(0,1),
            parking = randint(0,1),
            borne_service_rapide = randint(0,1),
            acces_handicap = randint(0,1),
            nombre_place = randint(20,100),
            departement = dep,
            pays_nom = random_pays,

            )
            conn.execute(insert_stmt)




with engine.begin() as conn :
    restoto = conn.execute(select([restaurant.c.restaurant_id,restaurant.c.code_postal])).fetchall()


with engine.begin() as conn:
    metier_list = ["cuisinier","caissier"]
    for i in range(len(restoto)):

        name = faker.name()
        insert_stmt = personnel.insert().values(
        metier = "directeur",
        note = 0,
        nom = faker.name(),
        adresse = faker.address(),
        experience = (randint(1,50)),
        manager = 'null',
        salaire = 10000,
        restaurant_id = restoto[i][0],
        code_postal = restoto[i][1]
        )
        conn.execute(insert_stmt)
        insert_stmt = personnel.insert().values(
        metier = "manager",
        note = 0,
        nom = name,
        adresse = faker.address(),
        experience = (randint(1,50)),
        manager = 'null',
        salaire = 3000,
        restaurant_id = restoto[i][0],
        code_postal = restoto[i][1]
        )
        conn.execute(insert_stmt)

        for _ in range(10):
            insert_stmt = personnel.insert().values(
            metier = choice(metier_list),
            note = randint(1,10),
            nom = faker.name(),
            adresse = faker.address(),
            experience = (randint(1,50)),
            manager = name,
            salaire = 1000,
            restaurant_id = restoto[i][0],
            code_postal = restoto[i][1]
            )
            conn.execute(insert_stmt)


# with engine.begin() as conn :
#     resto = conn.execute(select([restaurant.c.restaurant_id,restaurant.c.pays_nom,restaurant.c.code_postal,personnel.c.personne_id])).fetchall()  


# with engine.begin() as conn:
#     for _ in range(1000):
#         rd = randint(1,10000)
#         insert_stmt = commande.insert().values(
#             personne_id = resto[rd][3],
#             date = random_date(d1,d2),
#             pays_nom = resto[rd][1],
#             code_postal = resto[rd][2],
#             restaurant_id = resto[rd][0]
#         )
#         conn.execute(insert_stmt)


    










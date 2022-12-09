from sqlalchemy import MetaData,create_engine,select
from faker import Faker
from faker_food import FoodProvider
from random import randint,uniform,choice
from random import randrange
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta


def random_date(start, end):   #fonction qui génére une date aléatoire entre deux dates données
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

with engine.connect() as conn: #connection avec notre base de données existantes
    metadata.reflect(conn)


# récupération de des tables crées de notre bdd qu'on stock dans des variables
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

my_file = open("produit.txt", "r")  #récupération des noms d'items de ma liste txt qui contient des items de macdo
content = my_file.read()
produit_list = content.split(",")
my_file.close()





with engine.begin() as conn:
    for object in produit_list:         #insertion des produits et prix des items on boucle sur la produit list et on inseère item danas chaque ligne de produit id
        
        insert_stmt= produit.insert().values(
        produit_nom = object,
        prix = round(uniform(1.00,12.00),2))
        conn.execute(insert_stmt)




with engine.begin() as conn:
   for _ in range(40):
        insert_stmt= ingredient.insert().values(        #on créer 40 ingrédients avec faker food qu'on a importé au préalable
        ingredient_nom = faker.unique.ingredient(),
        prix = round(uniform(0.10,1.00),2))
        conn.execute(insert_stmt)

with engine.begin() as conn:
    for _ in range(26):                             #on insere les pays dans notre table pays
        insert_stmt = pays.insert().values(
        pays_nom = faker.unique.country()
        )
        conn.execute(insert_stmt)

with engine.begin() as conn :
    pa = conn.execute(select([pays.c.pays_nom])).fetchall()     #on récupère les pays dans une liste de tuple


number_list1 = [i for i in range(50000,99999)] #liste des code postaux générés

           
with engine.begin() as conn:            #on insère les codes postaux dans la table code postal et on enlève le code postal qui a été choisi pour crés des codes postaux uniques
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

for value in pa:                                    #je boucle sur ma liste de pays je séléctione un pays que je stocke dans une variable
    random_pays = value[0]
    number_list = [i for i in range(50000,99999)]       # je récupère ma liste de code postaux
    with engine.begin() as conn:
        for _ in range(10):
           
            n = choice(number_list)             #je choisis un code postal alétoire que j'enleve après avoir été choisi que je stock dans une variable
            number_list.remove(n)               
            number = str(n)                     # je stock dans une variable mon code postal choisi je transforme en string
            dep = int(number[:2])               # je prend les des premieres valeurs de mon code postal pour créer le département associé
            insert_stmt= restaurant.insert().values( #j'insère pour les données pour le restaurant
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
    restoto = conn.execute(select([restaurant.c.restaurant_id,restaurant.c.code_postal])).fetchall() # récupération du restaurant id et code_postal


with engine.begin() as conn:
    metier_list = ["cuisinier","caissier"]
    for i in range(len(restoto)): #je boucle sur la taille des restaurants

        name = faker.name()                                 #je stock le nom du manager dans une variable
        insert_stmt = personnel.insert().values(            #création du directeur
        metier = "directeur",
        note = 0,
        nom = faker.name(),     
        adresse = faker.address(),
        experience = (randint(1,50)),
        manager = 'null',
        salaire = 10000,
        restaurant_id = restoto[i][0],  #comme ma liste restotot est une liste de tuple on met le premier [] pour récupérer la valeur sans les tuples et on rajoute 
        code_postal = restoto[i][1]     #0 pour le restaurant id et 1 pour le code postal associé
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

        for _ in range(10):                             #on créer les 10 employés et on rajoute le nom du manager qu'on a choisi au départ , le manager est en charge des
            insert_stmt = personnel.insert().values(       # 10 employés crées
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

current_date = datetime.today()
with engine.begin() as conn :
    restototo = conn.execute(select([personnel.c.salaire,personnel.c.personne_id])).fetchall()
    exp  = conn.execute(select([personnel.c.experience])).fetchall()

with engine.begin() as conn:
    for i in range(len(exp)):
        n=exp[i][0]
        for j in range (n):
            insert_stmt = historique.insert().values(
            personne_id = restototo[i][1],
            Salaire = round(uniform(1400,1900),2),
            date = current_date - relativedelta(months=j),
            )
            conn.execute(insert_stmt)
                





with engine.begin() as conn :
    resto = conn.execute("""SELECT restaurant.restaurant_id,restaurant.pays_nom,restaurant.code_postal,personnel.personne_id 
                            FROM restaurant
                            JOIN personnel ON personnel.code_postal = restaurant.code_postal
    """).fetchall()


with engine.begin() as conn:

    for _ in range(1000):
        rd = randint(1,260)
        insert_stmt = commande.insert().values(
            personne_id = resto[rd][3],
            date = random_date(d1,d2),
            pays_nom = resto[rd][1],
            code_postal = resto[rd][2],
            restaurant_id = resto[rd][0]
        )
        conn.execute(insert_stmt)

with engine.begin() as conn:
    comm = conn.execute("""SELECT commande_id FROM commande""").fetchall()





with engine.begin() as conn : 
    for c in range(len(comm)):
        p_list = [i for i in len(produit_list)]
        number = (randint(2,5))
        for _ in range(number):
            p = choice(p_list)
            p_list.remove(p)
            insert_stmt = pc.insert().values(
            commande_id = c,
            produit_id = p,
            quantite = randint(1,3)
            )
            conn.execute(insert_stmt)

    










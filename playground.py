from faker import Faker
from faker.providers import BaseProvider
import random
f = Faker("fr_FR")

# ajouter une seed 

print(f.name())
print(f.address())
# print(f.zipcode()) pas utilisable pour la France X'( 

for _ in range(10):
    print(f.unique.random_int(min=1,max=10))

class tuned_provider(BaseProvider):

    def metier_rest(self):
        return random.choice(["Cuisinier","Serveur","Directeur","Manager"])
    # voir a quoi doit ressembler le personnel du restaurant 



f.add_provider(tuned_provider)
print(f.metier_rest())
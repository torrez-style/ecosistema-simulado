from ecosistema.organismos.organismo import Organismo
from ecosistema.organismos.planta import Planta
from ecosistema.organismos.herbivoro import Herbivoro
from ecosistema.organismos.carnivoro import Carnivoro

# Nombre de especie -> clase. Evita un if/elif por especie al poblar el
# mundo o al cargar una partida desde JSON.
ESPECIES = {
    "Planta": Planta,
    "Herbivoro": Herbivoro,
    "Carnivoro": Carnivoro,
}

__all__ = ["Organismo", "Planta", "Herbivoro", "Carnivoro", "ESPECIES"]

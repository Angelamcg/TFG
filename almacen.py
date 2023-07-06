# import os
# import django
# from django.conf import settings
# from API.models import Almacen

# # Configuración de Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto_TFG.settings')
# django.setup()

# # Crear almacen solo una vez
# pasillos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# estanterias = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# alturas = ['baja', 'media', 'alta']

# for pasillo in pasillos:
#     for estanteria in estanterias:
#         for altura in alturas:
#             nombre_foto = f'{pasillo}-{estanteria}.jpg'
#             foto_path = os.path.join(settings.STATIC_ROOT, 'almacen', nombre_foto)
#             if os.path.exists(foto_path):
#                 almacen_nombre = f'Almacen {pasillo}-{estanteria}-{altura}'
#                 almacen_filtrado = Almacen.objects.filter(nombre=almacen_nombre)
#                 if not almacen_filtrado.exists():
#                     almacen = Almacen(pasillo=pasillo, estanteria=estanteria, altura=altura, fotografia=f'almacen/{nombre_foto}')
#                     almacen.save()

# # Comprobacion

# almacenes = Almacen.objects.all()
# for almacen in almacenes:
#     print(almacen.pasillo)

# # almacen_filtrado = Almacen.objects.filter(nombre="MiAlmacen")
# # if almacen_filtrado.exists():
# #     print("El almacen existe en la base de datos")
# # else:
# #     print("El almacen no existe en la base de datos")

import os
import django
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from API.models import Almacen

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto_TFG.settings')
django.setup()

def crear_almacen():
    pasillos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    secciones = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    alturas = ['alta', 'media', 'baja']

    for pasillo in pasillos:
        for seccion in secciones:
            for altura in alturas:
                almacen_id = f'{pasillo}-{seccion}-{altura}'

                try:
                    Almacen.objects.get(id=almacen_id)
                    print(f"El almacen {almacen_id} ya existe en la base de datos.")
                except ObjectDoesNotExist:
                    almacen = Almacen(id=almacen_id, pasillo=pasillo, estanteria=seccion, altura=altura)
                    almacen.save()
                    print(f"Almacen {almacen_id} creado y guardado en la base de datos.")

if __name__ == "__main__":
    crear_almacen()

# Trabajo de Fin de Grado: Desarrollo de una aplicación web para gestión de inventario de una PYME

## Autora:Ángela María Carrasco García 
### Doble Grado en Ingeniería Informática y Administración de Empresas - Universidad de Granada

## Resumen 
El proyecto que se presenta a continuación tiene como objetivo cubrir la necesidad real de una Pequeña y Mediana Empresa (PYME) con problemas de inventario. La solución se trata de una aplicación web para el control de existencias en almacén. 
Las acciones principales de este proyecto consisten en gestionar los proveedores y clientes de la empresa en conjunto con sus transacciones (compras, ventas y devoluciones). Al conseguir un control directo con la entrada y salida de productos en almacén y permitir a los usuarios del sistema realizar acciones como realizar transacciones con productos, actualizar información y realizar búsquedas, se garantiza una gestión eficiente del inventario verificando en todo momento la cantidad y teniendo conocimiento de la ubicación en almacén de cada uno de los productos.
Asimismo, estos procesos se acompañan de una automatización de las facturas y de la cuenta de resultados de la empresa, para conseguir una visión clara de la situación financiera de la compañía.
Se espera que el resultado de esta aplicación web se vea reflejado en una automatización y centralización de datos en relación con el inventario de la empresa que permitirá la reducción de errores y el aumento de eficiencia y control de la empresa.
Para la gestión del proyecto se hará uso de la metodología ágil Scrum con la que se redactarán historias de usuario basadas en los requisitos funcionales solicitados por el cliente y que estarán organizadas por Sprints. En cuanto a la programación de la aplicación web se ha decidido que se utilizará el framework basado en el lenguaje de Python, Django. 

## Instalación 
1.	Ejecutar las migraciones para crear la estructura de la base de datos:
python3 manage.py makemigrations
python3 manage.py migrate

3.	Iniciar el servidor:
python3 manage.py runserver

5.	Abrir la aplicación en el navegador web en el link:
http://localhost:8000/

# Autor: Cristian Sáez Mardones
# Fecha: 20-03-2020
# Versión: 1.5.5
# Objetivo: Simular una pokedex consumiendo una API

# Importación de archivo
    # Si hay
# Importación de bibliotecas
    # Si hay
# Importación de funciones
    # No hay

# Importación de bibliotecas
import tkinter
from tkinter import ttk
import requests
import os
import base64
import urllib
import datetime

# Obtenemos la fecha formateada en la que se conectó para mantener registro
fecha_inicio = datetime.date.today().strftime('%d/%m/%Y')
# Obtenemos el tiempo del pc para poder calcular cuanto duró la conexión
inicio = datetime.datetime.now()
# Variable para registrar el total de operaciones realizadas
operaciones = 0
# Variable pare registrar cuantas operaciones fueron un éxito
exitos = 0
# Variable pare registrar cuantas operaciones fallaron
fallos = 0

# Ruta en donde se encuentra el archivo
ruta = os.path.dirname(os.path.abspath(__file__))
# Url a la que realizaremos peticiones get
url = 'https://pokeapi.co/api/v2/'

#####################################################################
# Función: Generar registro de las acciones realizadas
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def registrar(texto):
    with open(os.path.join(ruta, 'registro.txt'), 'a') as txt:
        txt.write(texto)

#####################################################################
# Función: Cerrar la aplicación
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def cerrar():
    root.destroy()

#####################################################################
# Función: Generar un registro de los tiempos de uso
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def generar_registro_final():
    fin = datetime.datetime.now()
    total = fin - inicio
    fecha_termino = datetime.date.today().strftime('%d/%m/%Y')
    texto = '========================================================\n'
    texto += f'La conexion se inicio en la fecha: {fecha_inicio}\n'
    texto += f'La conexion se termino en la fecha: {fecha_termino}\n'
    texto += f'Tiempo total de conexion: {total}\n'
    texto += f'Se realizaron un total de {operaciones} operaciones\n'
    texto += '========================================================\n'
    print(texto)
    registrar(texto)

#####################################################################
# Función: Vaciar el cuadro de texto
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def vaciar_text():
    text_info.configure(state=tkinter.NORMAL)
    text_info.delete(1.0, tkinter.END)
    text_info.configure(state=tkinter.DISABLED)

#####################################################################
# Función: Buscar un pokemon por nombre
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def busca_nombre():
    # Sumamos 1 a las operaciones realizadas
    global operaciones
    operaciones += 1
    # Obtenemos el nombre seleccionado para buscar
    nombre = nombre_pokemon.get()
    nombre = nombre.lower()
    busqueda_realizada = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    mensaje = f'Busqueda realizada: {busqueda_realizada}\nPokemon a buscar: {nombre}'
    # Tratamos de obtener la información del pokemon
    try:
        pokemons = requests.get(f'{url}pokemon/{nombre}')
        pokemons = pokemons.json()
        texto = f'Nombre: {nombre}\n'
        texto += '=============================================\n'
        texto += f'* Número en la pokedex: {pokemons["id"]}\n'
        texto += '=============================================\n'
        texto += f'* Experiencia base: {pokemons["base_experience"]}\n'
        texto += '=============================================\n'
        texto += 'Stats base:\n'
        for stat in pokemons['stats']:
            texto += f'* {stat["stat"]["name"]} - Base: {stat["base_stat"]}\n'
        texto += '=============================================\n'
        texto += 'Tipo(s):\n'
        for tipo in pokemons['types']:
            texto += f'* {tipo["type"]["name"]}\n' 
        texto += '=============================================\n'
        texto += f'* Altura: {pokemons["height"]}cm\n'
        texto += f'* Peso: {pokemons["weight"]}gr\n'

        # URL donde se encuentran las imagenes
        img1 = pokemons['sprites']['front_default']
        img2 = pokemons['sprites']['back_default']

        # Abrimos las imagenes
        with urllib.request.urlopen(img1) as u1:
            data1 = u1.read()

        with urllib.request.urlopen(img2) as u2:
            data2 = u2.read()

        # Convertimos las imagenes a base64 para poder mostrarlas
        b64_data1 = base64.encodebytes(data1)
        b64_data2 = base64.encodebytes(data2)

        # Posicionamos los label para poder mostrar las imagenes
        label_imagen_1.grid(row=0, column=0)
        label_imagen_2.grid(row=0, column=1)
        
        # Agregamos las imagenes para poder mostrarla
        image1.config(data=b64_data1)
        image2.config(data=b64_data2)
        # Agregamos el estado de éxito a nuestra busqueda
        mensaje += ' - Estado busqueda: Exito'
        # Si nuestra busqueda tiene éxito sumamos 1 al contador de éxito
        global exitos
        exitos += 1
    except:
        # En caso de fallo sumamos uno al contador de fallos
        texto = 'Ha ocurrido un error\nPor favor intente mas tarde o pruebe con otro pokemon'
        mensaje += ' - Estado busqueda: Fallo'
        # Quitamos cualquier imagen que pudiera haber en la aplicación
        label_imagen_1.grid_forget()
        label_imagen_2.grid_forget()
        # Sumamos 1 a nuestra variable de fallos
        global fallos
        fallos += 1
    finally:
        # Imprimimos el mensaje de éxito o fallo
        print(mensaje)
        # Registramos el mensaje en el archivo
        registrar(mensaje+'\n')

    # Vaciamos cualquier texto que pudiera haber en la aplicación
    vaciar_text()
    # Agregamos el resultado de la busqueda en el cuadro de texto
    text_info.configure(state=tkinter.NORMAL)
    text_info.insert(1.0, texto)
    text_info.configure(state=tkinter.DISABLED)

#####################################################################
# Función: Buscar tipo de pokemon
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def busca_tipo():
    busqueda_realizada = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    # Sumamos 1 a las operaciones realizadas
    global operaciones
    operaciones += 1
    # Obtenemos el tipo seleccionado para buscar
    tipo = tipo_pokemon.get()

    # Quitamos cualquier imagen que pudiera haber en la aplicación
    label_imagen_1.grid_forget()
    label_imagen_2.grid_forget()

    # Tratamos de obtener la información del pokemon
    try:
        tipo = tipo.lower()
        print(f'Tipo a buscar: {tipo}')
        pokemons = requests.get(f'{url}type/{tipo}')
        pokemons = pokemons.json()
        mensaje = f'La busqueda se realizo: {busqueda_realizada}\nEl tipo buscado es: {tipo}'
        texto = f'El tipo buscado es: {tipo}\n'
        texto += f'Existen {len(pokemons["pokemon"])} pokemons de tipo {tipo}\n'
        texto += f'Existen {len(pokemons["moves"])} movimientos de tipo {tipo}\n'
        if len(pokemons['damage_relations']['double_damage_from']) > 0:
            texto += 'Recibes doble daño de:\n'
            for tipo in pokemons['damage_relations']['double_damage_from']:
                texto += f'\t* {tipo["name"]}\n'
        if len(pokemons['damage_relations']['double_damage_to']) > 0:
            texto += 'Generas doble daño a:\n'
            for tipo in pokemons['damage_relations']['double_damage_to']:
                texto += f'\t* {tipo["name"]}\n'
        if len(pokemons['damage_relations']['half_damage_from']) > 0:
            texto += 'Recibes la mitad del daño de:\n'
            for tipo in pokemons['damage_relations']['half_damage_from']:
                texto += f'\t* {tipo["name"]}\n'
        if len(pokemons['damage_relations']['half_damage_to']) > 0:
            texto += 'Generas la mitad del daño a:\n'
            for tipo in pokemons['damage_relations']['half_damage_to']:
                texto += f'\t* {tipo["name"]}\n'
        if len(pokemons['damage_relations']['no_damage_from']) > 0:
            texto += 'No recibes daño de:\n'
            for tipo in pokemons['damage_relations']['no_damage_from']:
                texto += f'\t* {tipo["name"]}\n'
        if len(pokemons['damage_relations']['no_damage_to']) > 0:
            texto += 'No generas daño a:\n'
            for tipo in pokemons['damage_relations']['no_damage_to']:
                texto += f'\t* {tipo["name"]}\n'
        global exitos
        exitos += 1
        mensaje += ' - Estado busqueda: Exito'
    except:
        # En caso de fallo sumamos uno al contador de fallos
        texto = 'Ha ocurrido un error al realizar la busqueda'
        global fallos
        fallos += 1
        mensaje += ' - Estado busqueda: Fallo'
    finally:
        # Imprimimos el mensaje de éxito o fallo
        print(mensaje)
        # Registramos el mensaje en el archivo
        registrar(mensaje+'\n')
        
    # Vaciamos cualquier texto que pudiera haber en la aplicación
    vaciar_text()
    # Agregamos el resultado de la busqueda en el cuadro de texto
    text_info.configure(state=tkinter.NORMAL)
    text_info.insert(1.0, texto)
    text_info.configure(state=tkinter.DISABLED)

#####################################################################
# Función: Limpiar los campos de la interfaz grafica
# Entrada: No hay entrada en la función
# Salida: No hay salida de la función
def limpiar_campos():
    vaciar_text()
    nombre_pokemon.set('')
    tipo_pokemon.set('')
    label_imagen_1.grid_forget()
    label_imagen_2.grid_forget()

#####################################################################
# Función: Obtener los nombres de los pokemons desde la url
# Entrada: Url a la que se hara la petición
# Salida: Arreglo con los nombres de los pokemons
def obtener_nombres(url):
    # Hacemos la petición get
    pokemons = requests.get(url)
    # Convertimos la información a un json
    pokemons = pokemons.json()

    # Inicializamos una varaible para poder llevar la cuenta de los pokemons
    i = 1
    # Llamamos la variable global total parasaber la cantidad de pokemons registrados
    global total
    total = pokemons['count']
    # Creamos un arreglo para pode guardar los nombres de los pokemons
    names = list()

    # Creamos un ciclo while para poder recoger todos los pokemons
    while i <= total:
        # Creamos una llamada get la que nos trae 20 pokemons
        pokemons = requests.get(url)
        pokemons = pokemons.json()
        # Recogemos la url que contiene los siguientes pokemons
        url = pokemons['next']
        # Obtenemos los pokemons del json
        pokemons = pokemons['results']

        # Recorremos el arreglo para ver los pokemons
        for pokemon in pokemons:
            # Agregamos el nombre del pokemon a la lista names
            names.append(pokemon['name'])
        
        # Sumamos 20 a la variable i
        i+=20

    # Retornamos el arreglo con nombres
    return names

#####################################################################
# Función: Obtener los tipo de los pokemons desde la url
# Entrada: Url a la que se hara la petición
# Salida: Arreglo con los tipos de los pokemons
def obtener_tipos(url):
    # Hacemos la petición get
    pokemons = requests.get(url)
    # Convertimos la información a un json
    pokemons = pokemons.json()
    
    # Creamos un arreglo para pode guardar los nombres de los pokemons
    tipos = list()

    # Creamos una llamada get la que nos trae llos tipos
    pokemons_types = requests.get(url)
        # Obtenemos los tipos del json
    pokemons_types = pokemons['results']

    # Recorremos el arreglo para ver los tipos
    for tipo in pokemons_types:
        # Agregamos el nombre del tipo a la lista tipos
        tipos.append(tipo['name'])

    # Retornamos el arreglo con tipos
    return tipos


#######################
### Bloque principal###
#######################

# Se crea la interfaz gráfica
root = tkinter.Tk()
# Se agrega un titulo a la interfaz gráfica
root.title('Pokedex con Python')

print('Inicio de la petición GET')

# Se manda a llamar a las funciones para obtener los nombres y los tipos
names = obtener_nombres(url+'pokemon')
tipos = obtener_tipos(url+'type')

print('Fin de la petición GET')

# Variables para guardar al pokemon o tipo a buscar
nombre_pokemon = tkinter.StringVar()
tipo_pokemon = tkinter.StringVar()

# Creamos y empaquetamos los cuadros en donde se posicionarán los distintos elementos
cuadro1 = tkinter.Frame(root)
cuadro1.pack()
cuadro2 = tkinter.Frame(root)
cuadro2.pack()
cuadro3 = tkinter.Frame(root)
cuadro3.pack()

# Creamos los diferentes labels, combobox, button y text y los posicionamos
label_name = tkinter.Label(cuadro1, text='Nombre del pokemon')
label_name.grid(column=0, row=0, padx=5, pady=10)

box_name = ttk.Combobox(cuadro1, state='readonly', values=names, textvariable=nombre_pokemon)
box_name.grid(column=1, row=0, padx=5)

button_name = tkinter.Button(cuadro1, text='Buscar pokemon', command=busca_nombre)
button_name.grid(column=2, row=0, padx=5)

label_name = tkinter.Label(cuadro1, text='Tipo pokemon')
label_name.grid(column=0, row=1, padx=5, pady=10)

box_name = ttk.Combobox(cuadro1, state='readonly', values=tipos, textvariable=tipo_pokemon)
box_name.grid(column=1, row=1, padx=5)

button_name = tkinter.Button(cuadro1, text='Buscar tipo', command=busca_tipo)
button_name.grid(column=2, row=1, padx=5)

button_name = tkinter.Button(cuadro1, text='Vaciar campos', command=limpiar_campos)
button_name.grid(column=1, row=2, padx=5)

button_close = tkinter.Button(cuadro1, text='Cerrar', command=cerrar)
button_close.grid(column=1, row=3, padx=5, pady=5)

text_info = tkinter.Text(cuadro2, width=45, height=25)
text_info.grid(column=0, row=1, pady=5)
text_info.configure(state=tkinter.DISABLED)

# Elementos es donde se mostrarán las imagenes
image1 = tkinter.PhotoImage()
image2 = tkinter.PhotoImage()
label_imagen_1 = tkinter.Label(cuadro3, image=image1)
label_imagen_2 = tkinter.Label(cuadro3, image=image2)

# Iniciamos el loop de la GUI
root.mainloop()

# Al finalizar la gui creamos y mostramos el registro finals
generar_registro_final()
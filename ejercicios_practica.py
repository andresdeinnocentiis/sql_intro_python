#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3

# https://extendsclass.com/sqlite-browser.html


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('secundaria.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS estudiante;
            """)

    # Ejecutar una query
    c.execute("""
            CREATE TABLE estudiante(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [age] INTEGER NOT NULL,
                [grade] INTEGER,
                [tutor] TEXT
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

def crear_estudiante():
    estudiante = {}
    estudiante["name"] = (input("Ingrese el nombre del estudiante: ")).title()
    estudiante["age"] = int(input("Ingrese la edad del estudiante: "))
    estudiante["grade"] = int(input("Ingrese el año en que se encuentra el estudiante: "))
    estudiante["tutor"] = (input("Ingrese el tutor del estudiante: ")).title()

    if not estudiante["grade"]:
        estudiante["grade"] = "NULL"
    if not estudiante["tutor"]:
        estudiante["tutor"] = "NULL"
    print("CREAR ESTUDIANTE:\n", estudiante)
    return estudiante
    
def dic_estudiantes():
    cant = int(input("Ingrese la cantidad de estudiantes que desea cargar: "))
    estudiantes = {}
    for i in range(cant):
        print(f"- ESTUDIANTE {i+1}:\n")
        estudiantes[f"estudiante{str(i+1)}"] = crear_estudiante()
        print(f"Estudiante {i+1} cargado satisfactoriamente.\n")
    return estudiantes
    
def fill(estudiantes:dict):
    print('Completemos esta tablita!')
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> nombre de su tutor

    # Se debe utilizar la sentencia INSERT.
    # Observar que hay campos como "grade" y "tutor" que no son obligatorios
    # en el schema creado, puede obivar en algunos casos completar esos campos
    for estudiante, datos in estudiantes.items():
        print(estudiante)
        carga = list(datos.values())
        print(carga)
        c.execute("""
                INSERT INTO estudiante(name, age, grade, tutor)
                VALUES(?,?,?,?);""", carga)
        
    
    conn.commit()
    conn.close()
    
    
    
    
    
    

def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas
    # Utilizar fetchone para imprimir de una fila a la vez
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    c.execute('SELECT * FROM estudiante')
    
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)
    
    conn.close()

def search_by_grade(grade):
    print('Operación búsqueda!\n')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que se encuentra en en año "grade"

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    c.execute('SELECT id, name, age FROM estudiante WHERE grade = ?', (grade,))
    encontrados = 0
    while True:
        row = c.fetchone()
        if row is None:
            break
        else:
            encontrados += 1
            print(row)
    
    if encontrados == 0:
        print(f"No hay alumnos en {grade}° grado.")
    
    conn.close()


def insert(datos_estudiante:list=None):
    print('Nuevos ingresos!')
    # Utilizar la sentencia INSERT para ingresar nuevos estudiantes
    # a la secundaria
    continuar = False
    estudiante = {}
    if datos_estudiante == None:
        estudiante = crear_estudiante()
    else:
        for index, dato in enumerate(datos_estudiante):
            if not isinstance(dato, int):
                while not continuar:
                    rta = (input(f"'{dato}' es el nombre del alumno? [S/N]: ")).upper()
                    if rta != "S" and rta != "N":
                        print("La opción marcada es incorrecta.\n")
                    else:
                        if rta == "S":
                            estudiante["name"] = dato      
                            continuar = True
                            estudiante["tutor"] = input("Ingrese el nombre del tutor: ")
                            if not estudiante["tutor"]:
                                estudiante["tutor"] = "NULL"
                        else:
                            estudiante["tutor"] = dato   
                            estudiante["name"] = input("CAMPO OBLIGATORIO. Ingrese el nombre del alumno: ")
                            while not estudiante["name"]:
                                estudiante["name"] = input("CAMPO OBLIGATORIO. Ingrese el nombre del alumno: ")
                            continuar = True
                            
            else:
                continuar = False
                while not continuar:
                    rta = (input(f"'{dato}' es la edad del alumno? [S/N]: ")).upper()
                    if rta != "S" and rta != "N":
                        print("La opción marcada es incorrecta.\n")
                    else:
                        if rta == "S":

                            estudiante["age"] = dato 
                            estudiante["grade"] = input("Ingrese el año de curso del alumno: ")
                            if not estudiante["grade"]:
                                estudiante["grade"] = "NULL"     
                            continuar = True
                        else:
                            estudiante["age"] = None
                            estudiante["grade"] = dato   
                            while not continuar:
                                try:
                                    estudiante["age"] = int(input("CAMPO OBLIGATORIO. Ingrese la edad del alumno: "))
                                    continuar = True
                                except:
                                    print("Value Error. Solo se puede ingresar un valor de tipo INT.")
                                

    
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    carga = list(estudiante.values())
    print(carga)
    print(estudiante)
    c.execute("""
            INSERT INTO estudiante(name, age, grade, tutor)
            VALUES(?,?,?,?);""", (estudiante["name"],estudiante["age"],estudiante["grade"],estudiante["tutor"],))
    
    
    conn.commit()
    conn.close()


def modify(id=None, name=None):
    print('Modificando la tabla')
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar su nombre por "name" pasado como parámetro
    
    if not id:
        continuar = False
        while not continuar:
            try:
                id = int(input("CAMPO OBLIGATORIO. Ingrese el ID del alumno: "))
                continuar = True
            except:
                print("Value Error. Solo se puede ingresar un valor de tipo INT.") 
    
    if not name:
        continuar = False  
        while not name and not continuar:
            try:
                name = input("CAMPO OBLIGATORIO. Ingrese el nombre a modificar: ")
                continuar = True
            except:
                print("Value Error. Debe ingresar un nombre para modificar.") 
                       
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    rowcount = c.execute("UPDATE estudiante SET name =? WHERE id =?",
                         (name, id)).rowcount

    print('Filas actualizadas:', rowcount)
    
    conn.commit()
    conn.close()
    

if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    estudiantes = dic_estudiantes()
    fill(estudiantes)
    print("\n")
    fetch()
    print("\n")

    grade = 3
    search_by_grade(grade)
    print("\n")

    new_student = ['Batman', 45]
    insert(new_student) 
    
    #NOTAS: 
    # A) Programé la función para los casos en que:
    # 1. No se le pasen parámetros
    # 2. Se le pasen parámetros, pero como es una lista y no se puede saber a qué corresponden esos datos, 
    # y a su vez habría datos incompletos (y no se sabe si sería intencional o no), que pregunte a qué corresponde
    # dando la opción de cargar nuevos.
    
    # B) Cosas que consideré pero no programé porque ya me estaba desviando mucho del ejercicio:
    # 1. Para el caso que en la lista se pasen más de dos parámetros, o más de 4 parámetros, verificar/limpiar datos.
    # 2. Hacer una validación de datos más completa y manejar mejor las excepciones.
    
    print("\n")
    fetch()
    print("\n")
    search_by_grade(grade)
    print("\n")
    name = '¿Inove?'
    id = 2
    modify(name=name) # Programé la función considerando el caso en que no se le pase algún parámetro o ambos
    fetch()
    print("\n")

#!/usr/bin/env python
import openai
import json
import os
from dotenv import dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

# Funciones de historial y notas
def agregar_historial(mensaje, archivo="history.txt"):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(mensaje + "\n\n")

def guardar_nota(nota, archivo="notes.txt"):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(nota + "\n\n")

def limpiar_markdown(texto):
    """
    Elimina delimitadores Markdown (por ejemplo, ```json y ```) del texto.
    """
    lineas = texto.splitlines()
    if lineas and lineas[0].strip().startswith("```"):
        lineas = lineas[1:]
    if lineas and lineas[-1].strip().startswith("```"):
        lineas = lineas[:-1]
    return "\n".join(lineas).strip()

def obtener_memoria(archivo="history.txt", max_chars=2000):
    """
    Lee el archivo de historial y retorna los últimos 'max_chars' caracteres.
    Esto sirve para proporcionar contexto (memoria) en cada prompt.
    """
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            content = f.read()
        return content[-max_chars:] if len(content) > max_chars else content
    except Exception as e:
        return ""

def llamar_api_con_memoria(model, prompt, instructions, tools=[], stream=False):
    """
    Llama a la API de OpenAI agregando al prompt el contenido de la memoria (history.txt).
    """
    memoria = obtener_memoria()
    if memoria:
        prompt_total = memoria + "\n\n" + prompt
    else:
        prompt_total = prompt
    return openai.responses.create(
         model=model,
         input=prompt_total,
         instructions=instructions,
         tools=tools,
         stream=stream
    )

# Orquestador Fresh: divide la descripción en tareas
def orquestador_fresh(descripcion_proyecto):
    sistema = (
        "Eres Fresh, el orquestador. Eres un modelo gpt-4o-mini y tu tarea es dividir "
        "la descripción de un proyecto en subtareas específicas paso a paso. "
        "Cada subtarea debe incluir el lenguaje a utilizar ('python', 'nodejs' o 'rust'), "
        "el nombre del archivo a generar y una breve descripción de lo que debe contener ese archivo. "
        "Responde únicamente con un JSON que sea una lista de objetos. Por ejemplo:\n"
        '[{"lenguaje": "python", "archivo": "main.py", "descripcion": "Genera el script principal que administre ..."}, '
        '{"lenguaje": "nodejs", "archivo": "server.js", "descripcion": "Genera un servidor Express que ..."}]'
    )
    prompt = f"Descripción del proyecto: {descripcion_proyecto}\nGenera el plan de tareas."
    agregar_historial("Orquestador Fresh - Prompt:\n" + prompt)
    try:
        respuesta = llamar_api_con_memoria(
            model="gpt-4o-mini",
            prompt=prompt,
            instructions=sistema,
            tools=[],
            stream=False
        )
        output_text = respuesta.output_text.strip()
        output_text = limpiar_markdown(output_text)
        agregar_historial("Orquestador Fresh - Respuesta:\n" + output_text)
        plan = json.loads(output_text)
        return plan
    except Exception as e:
        error_msg = "Error en orquestador Fresh: " + str(e)
        print(error_msg)
        agregar_historial(error_msg)
        return []

# Agentes especializados para generar contenido
def generar_contenido_python(archivo, descripcion_tarea, proyecto_descripcion):
    prompt = (
        f"Eres un experto en desarrollo en Python. Genera el contenido del archivo '{archivo}' para un proyecto con la siguiente descripción: {proyecto_descripcion}. "
        f"El objetivo de este archivo es: {descripcion_tarea}. "
        "El contenido debe ser código Python funcional y bien comentado. Responde únicamente con el contenido del archivo."
    )
    agregar_historial(f"Agente Python - Prompt para {archivo}:\n" + prompt)
    try:
        respuesta = llamar_api_con_memoria(
            model="gpt-4o-mini",
            prompt=prompt,
            instructions="Genera el contenido sin ningún delimitador adicional.",
            tools=[],
            stream=False
        )
        contenido = limpiar_markdown(respuesta.output_text.strip())
        agregar_historial(f"Agente Python - Respuesta para {archivo}:\n" + contenido)
        return contenido
    except Exception as e:
        error_msg = f"Error al generar contenido para {archivo} en Python: {e}"
        print(error_msg)
        agregar_historial(error_msg)
        return ""

def generar_contenido_node(archivo, descripcion_tarea, proyecto_descripcion):
    prompt = (
        f"Eres un experto en desarrollo web con Node.js. Genera el contenido del archivo '{archivo}' para un proyecto con la siguiente descripción: {proyecto_descripcion}. "
        f"El objetivo de este archivo es: {descripcion_tarea}. "
        "El contenido debe ser código JavaScript/Node.js funcional y bien comentado. Responde únicamente con el contenido del archivo."
    )
    agregar_historial(f"Agente Node.js - Prompt para {archivo}:\n" + prompt)
    try:
        respuesta = llamar_api_con_memoria(
            model="gpt-4o-mini",
            prompt=prompt,
            instructions="Genera el contenido sin delimitadores.",
            tools=[],
            stream=False
        )
        contenido = limpiar_markdown(respuesta.output_text.strip())
        agregar_historial(f"Agente Node.js - Respuesta para {archivo}:\n" + contenido)
        return contenido
    except Exception as e:
        error_msg = f"Error al generar contenido para {archivo} en Node.js: {e}"
        print(error_msg)
        agregar_historial(error_msg)
        return ""

def generar_contenido_rust(archivo, descripcion_tarea, proyecto_descripcion):
    prompt = (
        f"Eres un experto en desarrollo en Rust. Genera el contenido del archivo '{archivo}' para un proyecto con la siguiente descripción: {proyecto_descripcion}. "
        f"El objetivo de este archivo es: {descripcion_tarea}. "
        "El contenido debe ser código Rust funcional y bien comentado. Responde únicamente con el contenido del archivo."
    )
    agregar_historial(f"Agente Rust - Prompt para {archivo}:\n" + prompt)
    try:
        respuesta = llamar_api_con_memoria(
            model="gpt-4o-mini",
            prompt=prompt,
            instructions="Genera el contenido sin ningún delimitador adicional.",
            tools=[],
            stream=False
        )
        contenido = limpiar_markdown(respuesta.output_text.strip())
        agregar_historial(f"Agente Rust - Respuesta para {archivo}:\n" + contenido)
        return contenido
    except Exception as e:
        error_msg = f"Error al generar contenido para {archivo} en Rust: {e}"
        print(error_msg)
        agregar_historial(error_msg)
        return ""

def crear_archivos_de_tareas(plan, ruta_base, proyecto_descripcion):
    for tarea in plan:
        lenguaje = tarea.get("lenguaje", "").lower()
        archivo = tarea.get("archivo", "archivo.txt")
        descripcion_tarea = tarea.get("descripcion", "")
        ruta_archivo = os.path.join(ruta_base, archivo)
        carpeta = os.path.dirname(ruta_archivo)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)
        contenido = ""
        if lenguaje == "python":
            contenido = generar_contenido_python(archivo, descripcion_tarea, proyecto_descripcion)
        elif lenguaje == "nodejs":
            contenido = generar_contenido_node(archivo, descripcion_tarea, proyecto_descripcion)
        elif lenguaje == "rust":
            contenido = generar_contenido_rust(archivo, descripcion_tarea, proyecto_descripcion)
        else:
            contenido = f"// Contenido para {archivo}: {descripcion_tarea}"
        print(f"Generando {archivo} ({lenguaje})...")
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        agregar_historial(f"Archivo creado: {ruta_archivo}")
        print(f"Archivo creado: {ruta_archivo}")

# Agente actualizador: lee un archivo y genera una versión mejorada
def actualizar_archivo(ruta_archivo, lenguaje):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido_original = f.read()
    except Exception as e:
        error_msg = f"Error al leer {ruta_archivo}: {e}"
        print(error_msg)
        agregar_historial(error_msg)
        return None

    prompt = (
        f"Eres un experto en desarrollo en {lenguaje}. Mejora y optimiza el siguiente código, "
        "agregando comentarios explicativos y corrigiendo posibles errores. "
        "Devuelve únicamente el código mejorado sin delimitadores.\n\n"
        f"{contenido_original}"
    )
    agregar_historial(f"Agente Actualizador - Prompt para {ruta_archivo}:\n" + prompt)
    try:
        respuesta = llamar_api_con_memoria(
            model="gpt-4o-mini",
            prompt=prompt,
            instructions="Genera el código mejorado sin ningún delimitador adicional.",
            tools=[],
            stream=False
        )
        contenido_mejorado = limpiar_markdown(respuesta.output_text.strip())
        agregar_historial(f"Agente Actualizador - Respuesta para {ruta_archivo}:\n" + contenido_mejorado)
        return contenido_mejorado
    except Exception as e:
        error_msg = f"Error al actualizar {ruta_archivo} en {lenguaje}: {e}"
        print(error_msg)
        agregar_historial(error_msg)
        return None

def actualizar_proyecto(ruta_origen, ruta_destino="playground_updated"):
    """
    Recorre el proyecto en 'ruta_origen', actualiza cada archivo mediante el agente actualizador
    y guarda la versión mejorada en 'ruta_destino', manteniendo la misma estructura.
    """
    for root, dirs, files in os.walk(ruta_origen):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in [".py", ".js", ".jsx", ".rs"]:
                # Determinar el lenguaje según la extensión
                if ext == ".py":
                    lenguaje = "Python"
                elif ext in [".js", ".jsx"]:
                    lenguaje = "Node.js"
                elif ext == ".rs":
                    lenguaje = "Rust"
                else:
                    lenguaje = "desconocido"
                ruta_archivo = os.path.join(root, file)
                print(f"Actualizando {ruta_archivo} ({lenguaje})...")
                contenido_actualizado = actualizar_archivo(ruta_archivo, lenguaje)
                if contenido_actualizado is not None:
                    rel_path = os.path.relpath(ruta_archivo, ruta_origen)
                    ruta_nueva = os.path.join(ruta_destino, rel_path)
                    nueva_carpeta = os.path.dirname(ruta_nueva)
                    if not os.path.exists(nueva_carpeta):
                        os.makedirs(nueva_carpeta, exist_ok=True)
                    with open(ruta_nueva, "w", encoding="utf-8") as f:
                        f.write(contenido_actualizado)
                    agregar_historial(f"Archivo actualizado: {ruta_nueva}")
                    print(f"Archivo actualizado: {ruta_nueva}")
            else:
                # Copiar archivos que no se actualizan
                ruta_archivo = os.path.join(root, file)
                rel_path = os.path.relpath(ruta_archivo, ruta_origen)
                ruta_nueva = os.path.join(ruta_destino, rel_path)
                nueva_carpeta = os.path.dirname(ruta_nueva)
                if not os.path.exists(nueva_carpeta):
                    os.makedirs(nueva_carpeta, exist_ok=True)
                with open(ruta_archivo, "r", encoding="utf-8") as fin, open(ruta_nueva, "w", encoding="utf-8") as fout:
                    contenido = fin.read()
                    fout.write(contenido)
                agregar_historial(f"Archivo copiado sin cambios: {ruta_nueva}")
                print(f"Archivo copiado sin cambios: {ruta_nueva}")

if __name__ == "__main__":
    # Paso 1: Crear el proyecto nuevo
    proyecto_descripcion = input("Introduce la descripción del proyecto: ")
    print("Orquestador Fresh generando el plan de tareas...")
    plan_tareas = orquestador_fresh(proyecto_descripcion)
    print("Plan de tareas generado:")
    print(json.dumps(plan_tareas, indent=4, ensure_ascii=False))
    
    ruta_proyecto = "playground"
    os.makedirs(ruta_proyecto, exist_ok=True)
    print("Generando archivos según el plan...")
    crear_archivos_de_tareas(plan_tareas, ruta_proyecto, proyecto_descripcion)
    print(f"El proyecto ha sido generado en la carpeta '{ruta_proyecto}'.")
    
    # Paso 2: Actualizar un proyecto existente (nuevo o proporcionado por el usuario)
    actualizar = input("¿Deseas actualizar un proyecto existente? (s/n): ").strip().lower()
    if actualizar == "s":
        ruta_existente = input("Introduce la ruta del proyecto a actualizar: ").strip()
        ruta_actualizada = "playground_updated"
        os.makedirs(ruta_actualizada, exist_ok=True)
        actualizar_proyecto(ruta_existente, ruta_actualizada)
        print(f"El proyecto actualizado se ha generado en la carpeta '{ruta_actualizada}'.")
    
    guardar_nota("Proceso finalizado para el proyecto: " + proyecto_descripcion)
    print("Historial guardado en 'history.txt' y notas en 'notes.txt'.")

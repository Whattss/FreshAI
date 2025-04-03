# FreshAI

FreshAI es un sistema de agentes orquestados diseñado para generar y actualizar proyectos de forma automática mediante modelos de inteligencia artificial. Utilizando un orquestador (Fresh) basado en gpt-4o-mini y agentes especializados en Python, Node.js y Rust, FreshAI facilita la creación de proyectos y la mejora de proyectos existentes. Además, implementa un mecanismo básico de "memoria" que inyecta parte del historial de interacciones (almacenado en history.txt) en cada solicitud, permitiendo que la IA tenga contexto acumulativo. Este proyecto es privado y se comparte únicamente entre personas de confianza.

    Nota: Este proyecto es privado. La API_KEY se gestiona mediante un archivo de entorno, por lo que es fundamental mantener el repositorio en un entorno seguro.

### Contenido del Proyecto

    agents.py: Script principal que integra:

        El orquestador Fresh para dividir la descripción del proyecto en tareas.

        Agentes especializados para generar el contenido de archivos en Python, Node.js y Rust.

        Un agente actualizador que lee y mejora proyectos existentes.

        Un mecanismo de memoria que inyecta contexto histórico (desde history.txt) en cada solicitud.

        Registro de todas las interacciones en history.txt y la posibilidad de guardar notas en notes.txt.

    playground/: Directorio donde se genera un nuevo proyecto basado en la descripción introducida.

    playground_updated/: Directorio donde se guarda la versión actualizada de un proyecto existente, si se opta por actualizar.

    history.txt: Archivo que almacena el historial de todos los prompts y respuestas procesados por FreshAI.

    notes.txt: Archivo para guardar notas o comentarios adicionales sobre el proceso.

### Prerrequisitos

    Python 3.7 o superior.

    pip (gestor de paquetes de Python).

    Una clave de API válida de OpenAI.

#### Instalación

    Clonar el repositorio:

```
git clone https://github.com/tu_usuario/FreshAI.git
cd FreshAI
```

### Instalar las dependencias:

Se requiere la biblioteca openai y dotenv para gestionar variables de entorno. Instálalos mediante:

```
pip install openai dotenv
```

### Crear el archivo de entorno:

Crea un fichero llamado .env en la raíz del proyecto y añade la siguiente línea, reemplazando <KEY> por tu clave de API de OpenAI:


    OPENAI_API_KEY=<KEY>

    El código de FreshAI está configurado para leer la clave de la API desde este archivo, de modo que no debas modificar la clave directamente en el código.

## Uso
Ejecución del Script

    Abre una terminal en la carpeta del proyecto y ejecuta:

```
python agents.py
```

### El sistema te solicitará que introduzcas la descripción del proyecto. Por ejemplo:

    Introduce la descripción del proyecto: Crear una aplicación multiplataforma para gestionar tareas, con un backend en Python, una interfaz web en Node.js y componentes críticos en Rust.

    FreshAI (a través del orquestador Fresh) generará un plan de tareas en formato JSON, dividiendo la descripción en subtareas (indicando el lenguaje, nombre del archivo y descripción de lo que debe contener).

    Los agentes especializados generarán el contenido de cada archivo y se creará la estructura en el directorio playground.

    Al finalizar, se te preguntará si deseas actualizar un proyecto existente. Si respondes "s", se solicitará la ruta del proyecto a actualizar y la versión mejorada se guardará en el directorio playground_updated.

## Memoria y Registro

    Memoria Contextual:
    Cada solicitud a la API incluye parte del historial almacenado en history.txt para proporcionar contexto acumulativo a la IA.

    Historial y Notas:

        Revisa history.txt para ver todos los prompts y respuestas procesadas.

        Usa notes.txt para documentar observaciones o comentarios sobre el proceso.

## Personalización

    Prompts y Modelos:
    Puedes modificar los prompts y las instrucciones en agents.py para adaptar el comportamiento de cada agente a las necesidades específicas de tu grupo.

    Extensiones:
    Si deseas agregar nuevos agentes para otros lenguajes o funcionalidades adicionales (por ejemplo, integración con bases de datos o despliegue automático), extiende el código en agents.py.

    Mecanismo de Memoria:
    El contexto se inyecta en cada solicitud leyendo los últimos caracteres de history.txt. Puedes ajustar la cantidad modificando el parámetro en la función obtener_memoria.

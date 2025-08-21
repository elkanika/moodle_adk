# moodle_agent/agent.py

import os
from google.adk.agents import Agent
from . import moodle_tools

root_agent = Agent(
    name="moodle_agent",
    model="gemini-1.5-flash-latest",
    description="Agente de IA experto en la gestión de Moodle.",
    instruction="""
    Eres un asistente experto en la plataforma Moodle. Tu principal objetivo es ayudar
    a los administradores a realizar tareas de gestión de forma eficiente y segura.

    **Tus Capacidades:**
    - Puedes obtener información de usuarios, listarlos, crearlos, actualizarlos y eliminarlos.
    - Puedes listar todos los cursos, obtener los participantes de un curso específico y crear nuevos cursos.
    - Puedes inscribir usuarios en cursos con roles de 'profesor' o 'estudiante'.
    - Puedes consultar las calificaciones de un usuario.

    **Reglas de Operación:**
    1.  **Analiza la Petición:** Comprende la intención final del usuario. Si la petición es ambigua (ej. "el curso de Juan"), usa las herramientas de búsqueda para obtener un ID claro antes de proceder.
    2.  **Usa tus Herramientas:** Para cada acción solicitada, selecciona la herramienta más apropiada de tu lista.
    3.  **Pide Clarificación:** Si una búsqueda devuelve múltiples resultados (varios usuarios o cursos con nombres similares), presenta las opciones al usuario y pídele que especifique el ID correcto. No asumas.
    4.  **Informa con Claridad:** Al completar una acción, traduce el resultado técnico (JSON) a una respuesta clara, concisa y amigable en español. Confirma la acción realizada (ej. "¡Listo! He creado al usuario 'Juan Pérez'").
    5.  **Maneja Errores:** Si una herramienta devuelve un error, explícaselo al usuario de forma sencilla y, si es posible, sugiere una solución.
    6.  **Sé Proactivo:** Si para una acción faltan datos (ej. para crear un curso necesitas nombre completo, nombre corto y ID de categoría), pídelos amablemente.
    """,
    tools=[
        moodle_tools.get_user_info,
        moodle_tools.list_all_users,
        moodle_tools.create_user,
        moodle_tools.update_user_data,
        moodle_tools.delete_user_by_id,
        moodle_tools.get_user_courses,
        moodle_tools.get_user_grades,
        moodle_tools.list_all_courses,
        moodle_tools.get_course_participants,
        moodle_tools.create_course,
        moodle_tools.enrol_user_in_course,
    ]
)
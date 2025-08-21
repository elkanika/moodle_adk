# moodle_agent/moodle_tools.py
from google.adk.tools.function_tool import FunctionTool
from .moodle_api import moodle_client
from typing import Optional
import json

# --- HERRAMIENTAS DE BÚSQUEDA Y RESOLUCIÓN ---

def find_user_by_name(name_query: str) -> tuple[dict | None, str | None]:
    """
    Función interna para buscar un usuario por nombre y manejar múltiples resultados.
    Devuelve el objeto de usuario si se encuentra uno único, o un mensaje de error/clarificación.
    """
    params = {"criteria[0][key]": "fullname", "criteria[0][value]": name_query}
    result = moodle_client.call('core_user_get_users', params)

    if not result or 'exception' in result or not result.get('users'):
        error_msg = result.get('message', 'No se encontraron usuarios.') if isinstance(result, dict) else 'Error desconocido.'
        return None, f"No encontré a nadie llamado '{name_query}'. Detalle: {error_msg}"
    
    users = result['users']
    if len(users) == 1:
        return users[0], None

    # Lógica para desambiguar si hay múltiples resultados
    name_query_lower = name_query.lower()
    exact_matches = [u for u in users if u.get('fullname', '').lower() == name_query_lower]
    if len(exact_matches) == 1:
        return exact_matches[0], None

    options = [f"- {u['fullname']} (ID: {u['id']})" for u in users[:10]]
    clarification_msg = (
        f"Encontré varios usuarios para '{name_query}'. "
        "Por favor, sé más específico o proporciona el ID del usuario correcto:\n" + "\n".join(options)
    )
    return None, clarification_msg

def find_course_by_name(course_name_query: str) -> tuple[dict | None, str | None]:
    """
    Función interna para buscar un curso y manejar la ambigüedad.
    """
    params = {"criterianame": "search", "criteriavalue": course_name_query}
    result = moodle_client.call('core_course_search_courses', params)

    if not result or not result.get('courses'):
        return None, f"No encontré ningún curso que coincida con '{course_name_query}'."
    
    courses = result['courses']
    if len(courses) == 1:
        return courses[0], None

    exact_matches = [c for c in courses if c.get('fullname', '').lower() == course_name_query.lower()]
    if len(exact_matches) == 1:
        return exact_matches[0], None
    
    options = [f"- {c['fullname']} (ID: {c['id']})" for c in courses]
    clarification_msg = (
        f"Encontré varios cursos para '{course_name_query}'. "
        "Por favor, especifica a cuál te refieres, si es necesario, usando su ID:\n" + "\n".join(options)
    )
    return None, clarification_msg

# --- HERRAMIENTAS EXPUESTAS AL AGENTE ---

@FunctionTool
def get_user_info(user_name: str) -> str:
    """
    Busca y devuelve la información completa de un usuario de Moodle por su nombre completo.
    Es útil para obtener el ID, email, etc., de una persona.
    """
    user, error = find_user_by_name(user_name)
    if error:
        return error
    return json.dumps(user)

@FunctionTool
def list_all_users() -> str:
    """
    Obtiene una lista de todos los usuarios registrados en la plataforma Moodle.
    """
    all_users = moodle_client.call('core_user_get_users', {"criteria[0][key]": "email", "criteria[0][value]": "%"})
    return json.dumps(all_users)

@FunctionTool
def create_user(username: str, firstname: str, lastname: str, email: str, password: str) -> str:
    """
    Crea un nuevo usuario en Moodle con los datos proporcionados. Se necesita un nombre de usuario,
    nombre, apellido, email y contraseña.
    """
    user_data = {
        "username": username, "password": password, "firstname": firstname,
        "lastname": lastname, "email": email, "auth": "manual"
    }
    params = {f"users[0][{k}]": v for k, v in user_data.items()}
    result = moodle_client.call('core_user_create_users', params)
    return json.dumps(result)

@FunctionTool
def update_user_data(user_id: int, new_email: Optional[str] = None, new_firstname: Optional[str] = None, new_lastname: Optional[str] = None) -> str:

    """
    Actualiza los datos de un usuario existente identificado por su ID.
    Puedes cambiar su email, nombre (firstname) o apellido (lastname).
    """
    update_data = {'id': user_id}
    if new_email: update_data['email'] = new_email
    if new_firstname: update_data['firstname'] = new_firstname
    if new_lastname: update_data['lastname'] = new_lastname
    
    if len(update_data) == 1:
        return "Error: Debes proporcionar al menos un dato para actualizar (email, nombre o apellido)."

    params = {f"users[0][{k}]": v for k, v in update_data.items()}
    result = moodle_client.call('core_user_update_users', params)
    return json.dumps(result)

@FunctionTool
def delete_user_by_id(user_id: int) -> str:
    """
    Elimina permanentemente a un usuario de Moodle usando su ID numérico.
    """
    result = moodle_client.call('core_user_delete_users', {'userids[0]': user_id})
    return json.dumps(result)

@FunctionTool
def get_user_courses(user_name: str) -> str:
    """
    Obtiene la lista de cursos en los que está inscrito un usuario, buscándolo por su nombre completo.
    """
    user, error = find_user_by_name(user_name)
    if error:
        return error
    
    result = moodle_client.call('core_enrol_get_users_courses', {'userid': user['id']})
    return json.dumps(result)

@FunctionTool
def get_user_grades(user_name: str) -> str:
    """
    Obtiene una vista general de las calificaciones de un usuario en todos sus cursos.
    """
    user, error = find_user_by_name(user_name)
    if error:
        return error
    
    result = moodle_client.call('gradereport_overview_get_course_grades', {'userid': user['id']})
    return json.dumps(result)

@FunctionTool
def list_all_courses() -> str:
    """
    Devuelve una lista con la información de todos los cursos disponibles en la plataforma Moodle.
    """
    courses = moodle_client.call('core_course_get_courses', {})
    # Filtramos cursos que no son visibles o son el "site" principal
    visible_courses = [c for c in courses if c.get('format') != 'site' and c.get('visible', True)]
    return json.dumps(visible_courses)

@FunctionTool
def get_course_participants(course_id: int) -> str:
    """
    Obtiene la lista completa de participantes (profesores y alumnos) de un curso específico,
    usando el ID del curso.
    """
    enrolled_users = moodle_client.call('core_enrol_get_enrolled_users', {'courseid': course_id})
    return json.dumps(enrolled_users)

@FunctionTool
def create_course(full_name: str, short_name: str, category_id: int) -> str:
    """
    Crea un nuevo curso en Moodle. Requiere un nombre completo, un nombre corto y el ID de la categoría.
    """
    course_data = {
        'fullname': full_name,
        'shortname': short_name,
        'categoryid': category_id
    }
    params = {f"courses[0][{k}]": v for k, v in course_data.items()}
    result = moodle_client.call('core_course_create_courses', params)
    return json.dumps(result)

@FunctionTool
def enrol_user_in_course(user_name: str, course_id: int, role: str) -> str:
    """
    Inscribe (matricula) a un usuario en un curso con un rol específico.
    Los roles válidos son 'student' (estudiante/alumno) o 'teacher' (profesor).
    """
    user, error = find_user_by_name(user_name)
    if error:
        return error

    role_map = {"teacher": 3, "profesor": 3, "student": 5, "estudiante": 5, "alumno": 5}
    role_id = role_map.get(role.lower())
    
    if not role_id:
        return "Error: Rol no válido. Usa 'student' o 'teacher'."

    params = {
        "enrolments[0][roleid]": role_id,
        "enrolments[0][userid]": user['id'],
        "enrolments[0][courseid]": course_id
    }
    result = moodle_client.call('enrol_manual_enrol_users', params)
    # La API no devuelve nada en caso de éxito, así que damos un mensaje genérico.
    if result is None:
        return json.dumps({"status": "success", "message": f"Usuario {user_name} inscrito en el curso {course_id}."})
    return json.dumps(result)
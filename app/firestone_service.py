import uuid
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users() -> list:
    """ Devuelve todos los usuarios """
    return db.collection('users').get()


def get_user_by_id(user_id):
    return db.collection('users')\
        .document(user_id).get()


def get_user(user_name):
    """Recibe el nombre de usuario, comprueba si existe luego envia los datos"""
    users_from_db = get_users()

    for user in users_from_db:
        if user.to_dict()['username'] == user_name:  # Comprueba si hay un nombre igual
            user_id = user.id
            return db.collection('users')\
                .document(user_id).get()
        else:
            return


def get_todos(user_id) -> list:
    """ Recibe el id, y devuelve todas las tareas """
    return db.collection('users')\
        .document(user_id)\
        .collection('todos').order_by('done').get()


def put_todo(user_id, description) -> None:
    """Recibe el id del usuario y el todo, para guardarlo en la bd"""

    todos_collection_ref = db.collection('users')\
        .document(user_id)\
        .collection('todos')

    # add genera un id aleatorio en firebase
    todos_collection_ref.add(
        {
            'descriptions': description,
            'done': False
        }
    )


def update_todo(user_id, todo_id, done):
    done_form = not bool(done)  # Recibe un numero y pasa a boleano
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': done_form})


def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()


# Agrega un nuevo usuario
def user_put(user_data) -> None:
    """ Recibe UserData, extaer los datos del usuario y los envia a la base de datos """

    user_ref = db.collection('users').document(user_data.user_id)
    user_ref.set(
        {
            'username': user_data.username,
            'password': user_data.password
        }
    )


def _get_todo_ref(user_id, todo_id):
    ref = db.document(f'users/{user_id}/todos/{todo_id}')
    return ref

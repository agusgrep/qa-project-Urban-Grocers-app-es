import pytest
from requests import status_codes

import configuration
import data
import requests

@pytest.fixture()
def create_user(): #FUNCION PARA COMPROBAR LA CREACION DE UN USUARIO
    response = requests.post(configuration.URL_SERVICE+configuration.CREATE_USER_PATH, headers=data.headers, json=data.user_body)

    assert response.status_code == 201
    return response.json()["authToken"]


def post_new_client_kit(kit_body, auth_token):
    # Copiamos los headers de data.py y le añadimos el token de autorización
    headers_copy = data.headers.copy()
    headers_copy["Authorization"] = f"Bearer {auth_token}"

    return requests.post(configuration.URL_SERVICE + configuration.KITS_PATH,
                         headers=headers_copy,
                         json=kit_body)


def get_kit_body(name):
    # Se copia el dict del kit para mantener aisladas las pruebas
    kit_body = data.kit.copy()
    kit_body["name"] = name
    return kit_body


def positive_assert(name, auth_token):
    kit_body = get_kit_body(name)
    response = post_new_client_kit(kit_body, auth_token)

    # Comprueba que el código de estado es 201
    assert response.status_code == 201
    # Comprueba que el campo "name" en la respuesta coincide con el de la solicitud
    assert response.json()["name"] == name


def negative_assert_code_400(kit_body, auth_token):
    response = post_new_client_kit(kit_body, auth_token)

    # Comprueba que el código de estado es 400
    assert response.status_code == 400


# -------------------------------------------------------
# Pruebas (Tests) de la Lista de Comprobación
# -------------------------------------------------------

# El número permitido de caracteres (1)
def test_kit_1_letter_in_name(create_user):
    positive_assert("a", create_user)


# El número permitido de caracteres (511)
def test_kit_511_letters_in_name(create_user):
    positive_assert(
        "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC",
        create_user)


# El número de caracteres es menor que la cantidad permitida (0)
def test_kit_empty_name_get_error(create_user):
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body, create_user)


# El número de caracteres es mayor que la cantidad permitida (512)
def test_kit_512_letters_in_name_get_error(create_user):
    kit_body = get_kit_body(
        "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
    negative_assert_code_400(kit_body, create_user)


# Se permiten caracteres especiales
def test_kit_has_special_symbol_in_name_get_success_response(create_user):
    positive_assert("\"№%@\",", create_user)


# Se permiten espacios
def test_kit_has_space_in_name_get_success_response(create_user):
    positive_assert(" A Aaa ", create_user)


# Se permiten números (como string)
def test_kit_has_numbers_in_name_get_success_response(create_user):
    positive_assert("123", create_user)


# El parámetro no se pasa en la solicitud
def test_create_kit_no_name_get_error_response(create_user):
    # Copiamos el body y eliminamos la clave "name" completamente
    kit_body = data.kit.copy()
    kit_body.pop("name")
    negative_assert_code_400(kit_body, create_user)


# Prueba 9: Se ha pasado un tipo de parámetro diferente (número)
def test_create_kit_number_type_name_get_error_response(create_user):
    kit_body = get_kit_body(123)
    negative_assert_code_400(kit_body, create_user)
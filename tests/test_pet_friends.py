from api import PetFriends
from setings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pets_with_valid_data(name='Барсик', anymal_type='кот',
                                      age='3', pet_photo='images/cat.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, anymal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Киска", "котя", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Маркиз', animal_type='Котик', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Самостоятельно написанные тесты. Добавлено 2 метода в PetFriends.


def test_simple_add_new_pet_with_valid_data(name='Джон', animal_type='пес', age='4'):
    """Проверяем возможность добавления питомца без фотографии"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo(pet_photo='images/dog.jpeg'):
    """Проверяем возможность добавления фотографии питомца."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] != ''


def test_get_api_key_for_incorrect_user(email='wrong@wrong', password='123'):
    """ Проверяем что запрос api ключа возвращает статус 403 при
    введениии некорректных данных"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pets_with_incorrect_photo(name='Барсик', animal_type='кот',
                                           age='3', pet_photo='images/cat2.gif'):
    """Проверяем что при попытке добавить питомца с некорректным типом фотографии возвращает
    статус 400. Это баг, питомец добавляется без фото и возвращается статус 200"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pets_with_incorrect_name(name=None, animal_type='кот', age='3',
                                          pet_photo='images/cat1.jpg'):
    """Проверяем что при попытке добавить питомца с некорректными именем возврщает статус 400.
    Это баг, питомец добавляется с пустыми полем имени  и возвращается статус 200"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pets_with_incorrect_animal_type(name='Барсик', animal_type=None, age='3',
                                                 pet_photo='images/cat1.jpg'):
    """Проверяем что при попытке добавить питомца с некорректными типом возврщает статус 400.
    Это баг, питомец добавляется с пустыми полем типа  и возвращается статус 200"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pets_with_incorrect_age(name='Барсик', animal_type='кот', age=None,
                                         pet_photo='images/cat1.jpg'):
    """Проверяем что при попытке добавить питомца с некорректными возрастом возврщает статус 400.
    Это баг, питомец добавляется с пустыми полем восраста  и возвращается статус 200"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_update_pets_with_incorrect_age(name='Маркиз', animal_type='Котик', age=-5):
    """Проверяем что произойдет при обновлении информации с указанием
    отрицательного возраста животного"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status != 200
    else:
        raise Exception("There is no my pets")


def test_add_new_pets_with_incorrect_auth_key(name='Барсик', anymal_type='кот',
                                              age='3', pet_photo='images/cat.jpeg'):
    """Проверяем что произойдет при попытке добавить питомца используя некорректный auth_key.
    Создан метод add_new_pet_with_incorrect_auth_key в классе PetFriends. """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = '123'
    status, result = pf.add_new_pet_with_incorrect_auth_key(auth_key, name, anymal_type, age, pet_photo)
    assert status == 403

from core.folders.domain.value_objects.box import LockedBox, OpenBox
from core.folders.domain.value_objects.encryption import EncryptionWarehouse
from core.folders.tests.helpers.car import CarWithSecretName
from core.folders.tests.helpers.encryptions import (
    SymmetricEncryptionTest1,
    SymmetricEncryptionTest2,
)
from core.other.deprecated.content_upgrade import Content


def test_encrypt_and_decrypt(single_encryption, car_content_key):
    car, content, key = car_content_key
    assert isinstance(car.name, LockedBox)
    assert car.name != b"BMW"
    content.decrypt(key)
    assert isinstance(car.name, OpenBox)
    assert car.name == b"BMW"


def test_encryption_hierarchy_works_in_simple_case(single_encryption, car_content_key):
    car, content, key = car_content_key

    assert isinstance(car.name, LockedBox)
    assert car.name != b"BMW"
    content.decrypt(key)
    assert isinstance(car.name, OpenBox)
    assert car.name == b"BMW"
    assert b"BMW" in SymmetricEncryptionTest1.get_treasure_chest().values()
    EncryptionWarehouse.add_symmetric_encryption(SymmetricEncryptionTest2)
    assert b"BMW" not in SymmetricEncryptionTest2.get_treasure_chest().values()
    content.encrypt()
    assert b"BMW" in SymmetricEncryptionTest2.get_treasure_chest().values()


def test_encryption_hierarchy_works_after_new_init(double_encryption, car_content_key):
    car, content, key = car_content_key

    content = Content("My Car", car, content.encryption_version)
    content.decrypt(key)

    assert isinstance(car.name, OpenBox)
    assert car.name == b"BMW"

    content.encrypt()
    assert content.encryption_version == "ST2"
    assert b"BMW" in SymmetricEncryptionTest2.get_treasure_chest().values()


def test_content_after_encryption(double_encryption, car_content_key):
    car, content, key = car_content_key

    car2 = CarWithSecretName(enc_name=car.name)
    content = Content("My Car", car2, content.encryption_version)
    content.decrypt(key)

    assert car2.name == b"BMW"


def test_item_and_name(single_encryption, car_content_key):
    car, content, key = car_content_key

    assert content.item == car
    assert content.name == "My Car"
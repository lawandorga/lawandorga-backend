#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2020  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

from rest_framework.test import APIClient
from backend.api.models import UserEncryptionKeys, UserProfile, Rlc, Group, Permission, RlcEncryptionKeys, UsersRlcKeys, HasPermission
from backend.static.encryption import RSAEncryption, AESEncryption
from backend.static.permissions import get_all_permissions_strings
from backend.files.static.folder_permissions import get_all_folder_permissions_strings
from backend.files.models import FolderPermission
from backend.api.errors import CustomError
from backend.static.error_codes import ERROR__API__HAS_PERMISSION__NOT_FOUND


class CreateFixtures:
    @staticmethod
    def create_base_fixtures():
        """

        :return: Accessible:
        User0: {return object}['users'][0]['user']
        User0 private key: {return object}['users'][0]['private']
        User0 client: {return object}['users'][0]['client']
        Rlc0 of users: {return object}['rlc']
        Group0: {return object}['groups'][0]
        """

        CreateFixtures.create_permissions()
        return_object = {}

        rlc = Rlc(name="testrlc", id=3001)
        rlc.save()
        rlc_aes_key = 'SecureAesKey'
        private, public = RSAEncryption.generate_keys()
        encrypted_private = AESEncryption.encrypt(private, rlc_aes_key)
        rlc_keys = RlcEncryptionKeys(rlc=rlc, encrypted_private_key=encrypted_private, public_key=public)
        rlc_keys.save()
        return_object.update({"rlc": rlc})

        users = []
        users.append(CreateFixtures.create_user(rlc, "user1", rlc_aes_key))
        users.append(CreateFixtures.create_user(rlc, "user2", rlc_aes_key))
        users.append(CreateFixtures.create_user(rlc, "user3", rlc_aes_key))
        users.append(CreateFixtures.create_user(rlc, "user4", rlc_aes_key))
        return_object.update({"users": users})

        groups = []
        groups.append(CreateFixtures.create_group(rlc, 'group1', [users[0]['user'], users[1]['user']]))
        groups.append(CreateFixtures.create_group(rlc, 'group2', [users[1]['user'], users[2]['user']]))
        groups.append(CreateFixtures.create_group(rlc, 'group3', [users[2]['user'], users[3]['user']]))
        return_object.update({'groups': groups})

        return return_object

    @staticmethod
    def create_user(rlc, name, rlc_aes_key):
        user = UserProfile(name=name, email=name + "@law-orga.de", rlc=rlc)
        user.set_password("qwe123")
        user.save()
        private, public = RSAEncryption.generate_keys()
        keys = UserEncryptionKeys(user=user, private_key=private, public_key=public)
        keys.save()

        encrypted_rlcs_key = RSAEncryption.encrypt(rlc_aes_key, public)
        rlcs_keys = UsersRlcKeys(user=user, rlc=rlc, encrypted_key=encrypted_rlcs_key)
        rlcs_keys.save()

        client = APIClient()
        client.force_authenticate(user=user)
        return {
            "user": user,
            "private": private,
            "client": client
        }

    @staticmethod
    def create_group(rlc, name, members):
        group = Group(name=name, from_rlc=rlc, visible=True)
        group.save()

        for member in members:
            group.group_members.add(member)
        return group

    @staticmethod
    def create_permissions():
        perms = get_all_permissions_strings()
        for perm in perms:
            Permission.objects.create(name=perm)
        perms = get_all_folder_permissions_strings()
        for perm in perms:
            FolderPermission.objects.create(name=perm)

    @staticmethod
    def create_superuser():
        """

        :return: Accessible:
        Superuser: {return object}['user']
        Superusers private key: {return object}['[private']
        Superusers client: {return object}['client']
        """
        superuser = UserProfile(name='superuser', email='superuser@test.de', is_superuser=True)
        superuser.set_password('qwe123')
        superuser.save()
        private, public = RSAEncryption.generate_keys()
        keys = UserEncryptionKeys(user=superuser, private_key=private, public_key=public)
        keys.save()
        client = APIClient()
        client.force_authenticate(user=superuser)
        return {
            "user": superuser,
            "private": private,
            "client": client
        }

    @staticmethod
    def add_permission_for_user(user, permission):
        """

        :param user: User
        :param permission: permissions string
        :return:
        """
        try:
            perm = Permission.objects.get(name=permission)
        except:
            raise CustomError(ERROR__API__HAS_PERMISSION__NOT_FOUND)

        has_perm = HasPermission(user_has_permission=user, permission_for_rlc=user.rlc, permission=perm)
        has_perm.save()


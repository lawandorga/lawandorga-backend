from typing import List, Optional

from django.conf import settings

from core.auth.domain.user_key import UserKey
from core.auth.models import StatisticUser
from core.models import RlcUser, UserProfile
from core.records.models import Record, RecordEncryptionNew, RecordTemplate
from core.rlc.models import Org
from core.seedwork.encryption import AESEncryption


def create_org(name="Dummy RLC"):
    org = Org.objects.create(name=name)
    return org


def create_statistics_user(email="dummy@law-orga.de", name="Dummy 1"):
    user = UserProfile.objects.create(email=email, name=name)
    user.set_password(settings.DUMMY_USER_PASSWORD)
    user.save()
    statistics_user = StatisticUser.objects.create(user=user)
    return {
        "user": user,
        "username": user.email,
        "email": user.email,
        "password": settings.DUMMY_USER_PASSWORD,
        "statistics_user": statistics_user,
    }


def create_user(email="dummy@law-orga.de", name="Mr. Dummy"):
    user = UserProfile.objects.create(email=email, name=name)
    user.set_password(settings.DUMMY_USER_PASSWORD)
    user.save()
    return user


def create_rlc_user(
    email="dummy@law-orga.de",
    name="Dummy 1",
    rlc=None,
    accepted=True,
    password=settings.DUMMY_USER_PASSWORD,
):
    user = UserProfile.objects.create(email=email, name=name)
    user.set_password(password)
    user.save()
    rlc_user = RlcUser(user=user, email_confirmed=True, accepted=accepted, org=rlc)
    rlc_user.generate_keys(password)
    rlc_user.save()
    private_key = (
        UserKey.create_from_dict(rlc_user.key)
        .decrypt_self(password)
        .key.get_private_key()
        .decode("utf-8")
    )
    return {
        "user": user,
        "username": user.email,
        "email": user.email,
        "password": settings.DUMMY_USER_PASSWORD,
        "rlc_user": rlc_user,
        "private_key": private_key,
        "public_key": user.get_public_key(),
    }


def create_record_template(org=None):
    template = RecordTemplate.objects.create(rlc=org, name="Record Template")
    return {"template": template}


def create_record(template=None, users: Optional[List[UserProfile]] = None):
    if template is None and users is not None and len(users):
        template = RecordTemplate.objects.create(
            rlc=users[0].rlc, name="Record Template"
        )
    record = Record.objects.create(template=template)
    aes_key_record = AESEncryption.generate_secure_key()
    for user in users if users else []:
        public_key_user = user.get_public_key()
        encryption = RecordEncryptionNew(
            record=record, user=user.rlc_user, key=aes_key_record
        )
        encryption.encrypt(public_key_user=public_key_user)
        encryption.save()
    return {"record": record, "aes_key": aes_key_record}

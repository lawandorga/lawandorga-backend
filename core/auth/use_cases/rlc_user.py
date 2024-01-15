from smtplib import SMTPRecipientsRefused

from django.db import transaction

from core.auth.models import OrgUser, UserProfile
from core.auth.token_generator import EmailConfirmationTokenGenerator
from core.auth.use_cases.finders import (
    org_from_id_dangerous,
    org_user_from_id_dangerous,
    rlc_user_from_id,
)
from core.legal.models import LegalRequirement, LegalRequirementEvent
from core.permissions.static import PERMISSION_ADMIN_MANAGE_USERS
from core.seedwork.use_case_layer import UseCaseError, use_case


@use_case
def register_rlc_user(
    __actor: None,
    email: str,
    password: str,
    name: str,
    accepted_legal_requirements: list[int],
    org_id: int,
):
    org = org_from_id_dangerous(__actor, org_id)

    # error validation
    if UserProfile.objects.filter(email=email).exists():
        raise UseCaseError("An account already exists with this email.")

    # user stuff
    user = UserProfile(email=email, name=name)
    user.set_password(password)
    rlc_user = OrgUser(user=user, email_confirmed=False, org=org)
    rlc_user.generate_keys(password)

    # legal stuff
    lr_events = []
    for lr in list(LegalRequirement.objects.all()):
        if lr.accept_required and lr.pk not in accepted_legal_requirements:
            raise UseCaseError(
                "You need to accept the legal requirement: '{}'.".format(lr.title)
            )
        event = LegalRequirementEvent(
            legal_requirement=lr,
            user=rlc_user,
            actor=email,
            accepted=True,
            text="Accepted on registration.",
        )
        lr_events.append(event)

    # save
    with transaction.atomic():
        user.save()
        rlc_user.save()
        for lre in lr_events:
            lre.save()
        assert rlc_user.key is not None

    # send confirmation mail
    try:
        rlc_user.send_email_confirmation_email()
    except SMTPRecipientsRefused:
        user.delete()
        raise UseCaseError(
            "We could not send a confirmation email to this address. "
            "Please check if this email is correct."
        )


@use_case(permissions=[PERMISSION_ADMIN_MANAGE_USERS])
def delete_user(__actor: OrgUser, other_user_id: int):
    other_user = rlc_user_from_id(__actor, other_user_id)
    if not other_user.check_delete_is_safe():
        raise UseCaseError(
            "You can not delete this user right now, because "
            "you could loose access to one or "
            "more folders. This user is one of the only two "
            "persons with access to those folders."
        )
    other_user.user.delete()


@use_case
def confirm_email(__actor: None, rlc_user_id: int, token: str):
    rlc_user = org_user_from_id_dangerous(__actor, rlc_user_id)
    rlc_user.confirm_email(EmailConfirmationTokenGenerator, token)
    rlc_user.save()


@use_case
def unlock_user(__actor: OrgUser, another_rlc_user_id: int):
    another_rlc_user = rlc_user_from_id(__actor, another_rlc_user_id)
    another_rlc_user.unlock(__actor)
    another_rlc_user.save()


@use_case
def unlock_myself(__actor: OrgUser):
    __actor.user.test_all_keys(__actor.get_private_key())
    if not __actor.all_keys_correct:
        raise UseCaseError(
            "You can only unlock yourself when all your keys are correct.",
        )
    __actor.locked = False
    __actor.save()

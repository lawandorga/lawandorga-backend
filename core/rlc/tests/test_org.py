import json

import pytest
from django.test import Client

from core.models import Org
from core.rlc.models import ExternalLink
from core.seedwork import test_helpers as data
from core.static import PERMISSION_ADMIN_MANAGE_USERS


@pytest.fixture
def org(db):
    org = Org.objects.create(name="Test RLC")
    yield org


@pytest.fixture
def user(db, org):
    user = data.create_rlc_user(rlc=org)
    org.generate_keys()
    ExternalLink.objects.create(
        org=org, name="Test Link", link="https://www.amazon.de", order=1
    )
    yield user


def test_list_links_works(user, db):
    c = Client()
    c.login(**user)
    response = c.get("/api/org/links/")
    response_data = response.json()
    assert response.status_code == 200 and len(response_data) == 1


def test_create_link_works(user, db):
    c = Client()
    c.login(**user)
    response = c.post(
        "/api/org/links/",
        data=json.dumps({"name": "New Link", "link": "https://ebay.de", "order": 2}),
        content_type="application/json",
    )
    response_data = response.json()
    assert response.status_code == 200 and response_data["name"] == "New Link"


def test_delete_link_works(user, db):
    c = Client()
    c.login(**user)
    link = user["rlc_user"].org.external_links.first()
    response = c.delete("/api/org/links/{}/".format(link.id))
    assert response.status_code == 200


def test_member_accept(user, db):
    c = Client()
    c.login(**user)
    user["rlc_user"].grant(PERMISSION_ADMIN_MANAGE_USERS)
    another_user = data.create_rlc_user(
        rlc=user["rlc_user"].org, email="another@law-orga.de"
    )
    response = c.post(
        "/api/org/accept_member/",
        json.dumps({"user": another_user["rlc_user"].id}),
        content_type="application/json",
    )
    assert response.status_code == 200

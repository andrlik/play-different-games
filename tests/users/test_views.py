# test_views.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize(
    "view_name",
    [
        "user-detail",
        "user-edit",
    ],
)
def test_unauthorized_get_views(
    client, django_assert_max_num_queries, tp, user, view_name
):
    url = tp.reverse(f"users:{view_name}", username=user.username)
    with django_assert_max_num_queries(25):
        response = client.get(url)
    assert response.status_code == 302
    assert "accounts/login" in response["Location"]


def test_unauthorized_post_views(client, django_assert_max_num_queries, tp, user):
    url = tp.reverse("users:user-edit", username=user.username)
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "timezone": "America/New_York",
    }
    with django_assert_max_num_queries(25):
        response = client.post(url, data=data)
    assert response.status_code == 302
    assert "accounts/login" in response["Location"]
    user.refresh_from_db()
    assert user.first_name != "John"
    assert user.profile.timezone != "America/New_York"


@pytest.mark.parametrize(
    "view_name",
    [
        "user-detail",
        "user-edit",
    ],
)
def test_authorized_no_permission_views(
    client, django_assert_max_num_queries, tp, user, view_name
):
    url = tp.reverse(f"users:{view_name}", username=user.username)
    user2 = tp.make_user("u2")
    client.force_login(user2)
    with django_assert_max_num_queries(25):
        response = client.get(url)
    assert response.status_code == 403


def test_authorized_no_permission_user_edit(
    client, django_assert_max_num_queries, tp, user
):
    url = tp.reverse("users:user-edit", username=user.username)
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "timezone": "America/New_York",
    }
    user2 = tp.make_user("u2")
    client.force_login(user2)
    with django_assert_max_num_queries(25):
        response = client.post(url, data=data)
    assert response.status_code == 403
    user.refresh_from_db()
    assert user.first_name != "John"
    assert user.profile.timezone != "America/New_York"


@pytest.mark.parametrize(
    "view_name",
    [
        "user-detail",
        "user-edit",
    ],
)
def test_authorized_has_permission_get_views(
    client, django_assert_max_num_queries, tp, user, view_name
):
    url = tp.reverse(f"users:{view_name}", username=user.username)
    client.force_login(user)
    with django_assert_max_num_queries(25):
        response = client.get(url)
    assert response.status_code == 200
    user2 = tp.make_user("u2")
    user2.is_staff = True
    user2.is_superuser = True
    user2.save()
    client.force_login(user2)
    with django_assert_max_num_queries(25):
        response = client.get(url)
    assert response.status_code == 200


def test_authorized_has_permission_post_views(
    client, django_assert_max_num_queries, tp, user
):
    url = tp.reverse("users:user-edit", username=user.username)
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "timezone": "America/New_York",
    }
    client.force_login(user)
    with django_assert_max_num_queries(25):
        response = client.post(url, data=data)
    assert response.status_code == 302
    assert (
        tp.reverse("users:user-detail", username=user.username) in response["Location"]
    )
    user.refresh_from_db()
    assert user.first_name == "John"
    assert user.profile.timezone == "America/New_York"
    user2 = tp.make_user("u2")
    user2.is_staff = True
    user2.is_superuser = True
    user2.save()
    client.force_login(user2)
    data["timezone"] = "America/Chicago"
    with django_assert_max_num_queries(25):
        response = client.post(url, data=data)
    assert response.status_code == 302
    assert (
        tp.reverse("users:user-detail", username=user.username) in response["Location"]
    )
    user.refresh_from_db()
    assert user.profile.timezone == "America/Chicago"

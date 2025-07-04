from flask.testing import FlaskClient

from flaskr.models.route import DayVariant
from flaskr.models.user import User
from flaskr.models.trip import TripParticipant, TripSession, TripVote


def test_vote_if_is_participant(
    users: list[User],
    participants_different_admin_count: list[list[TripParticipant]],
    variants: list[list[DayVariant]],
    multiply_sessions: list[TripSession],
    client: FlaskClient,
):
    """
    Если пользователь проголосует в поездке,
    к которой имеет доступ, то успешно (200)
    """
    with client.session_transaction() as session:
        session["uuid"] = users[0].uuid

    choices = [
        {variants[0][0].id: variants[0][0].day.day_order},
        {variants[1][0].id: variants[1][0].day.day_order},
        {variants[2][1].id: variants[2][1].day.day_order},
    ]
    resp = client.post(
        "/api/session/vote",
        json={"choices": choices, "session_id": multiply_sessions[0].id},
    )

    assert resp.status_code == 200  # Успешно
    expected_votes = [
        {
            "session_id": multiply_sessions[0].id,
            "variant_id": variants[0][0].id,
            "participant_id": participants_different_admin_count[0][0].id,
            "day_order": variants[0][0].day.day_order,
        },
        {
            "session_id": multiply_sessions[0].id,
            "variant_id": variants[1][0].id,
            "participant_id": participants_different_admin_count[0][0].id,
            "day_order": variants[1][0].day.day_order,
        },
        {
            "session_id": multiply_sessions[0].id,
            "variant_id": variants[2][1].id,
            "participant_id": participants_different_admin_count[0][0].id,
            "day_order": variants[2][1].day.day_order,
        },
    ]

    for expected_vote, returned_vote in zip(expected_votes, resp.json["votes"]):
        assert expected_vote == returned_vote


def test_vote_if_is_not_participant(
    users: list[User],
    participants_different_admin_count: list[list[TripParticipant]],
    variants: list[list[DayVariant]],
    multiply_sessions: list[TripSession],
    client: FlaskClient,
):
    """
    Если пользователь проголосует в поездке,
    к которой не имеет доступа, то отказано в доступе (403)
    """
    with client.session_transaction() as session:
        session["uuid"] = users[0].uuid

    choices = [
        {variants[0][0].id: variants[0][0].day.day_order},
        {variants[1][0].id: variants[1][0].day.day_order},
        {variants[2][1].id: variants[2][1].day.day_order},
    ]
    resp = client.post(
        "/api/session/vote",
        json={"choices": choices, "session_id": multiply_sessions[2].id},
    )

    assert resp.status_code == 403  # отказано в доступе


def test_vote_when_voting_is_finished(
    users: list[User],
    participant_votes: list[list[TripVote]],
    variants: list[list[DayVariant]],
    session: TripSession,
    client: FlaskClient,
):
    """
    Если пользователь проголосует,
    когда голосование завершилось, то отказано (422)
    """
    with client.session_transaction() as fk_session:
        fk_session["uuid"] = users[0].uuid

    choices = [
        {variants[0][0].id: variants[0][0].day.day_order},
        {variants[1][0].id: variants[1][0].day.day_order},
        {variants[2][1].id: variants[2][1].day.day_order},
    ]
    resp = client.post(
        "/api/session/vote", json={"choices": choices, "session_id": session.id}
    )

    assert resp.status_code == 422  # голосование завершилось

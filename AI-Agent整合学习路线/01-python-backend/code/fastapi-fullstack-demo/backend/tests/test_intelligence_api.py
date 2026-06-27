from sqlmodel import Session, SQLModel, create_engine

from app.core import database as _database  # noqa: F401
from app.routers.intelligence import get_home, list_categories, seed_demo_content


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_public_home_endpoint_returns_seeded_shape():
    session = make_session()
    response = get_home(session=session)

    payload = response.data
    assert "latest_items" in payload
    assert "categories" in payload
    assert "brief" in payload


def test_public_categories_endpoint_lists_navigation_labels():
    response = list_categories()

    labels = response.data
    assert "Agent" in labels
    assert "RAG" in labels


def test_seed_demo_content_makes_home_non_empty():
    session = make_session()

    seed_response = seed_demo_content(session=session)
    home_response = get_home(session=session)

    assert seed_response.data["created"] == 2
    assert len(home_response.data["latest_items"]) == 2
    assert home_response.data["brief"] is not None

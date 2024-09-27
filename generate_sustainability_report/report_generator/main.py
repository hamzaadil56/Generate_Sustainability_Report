from langchain_community.document_loaders.sql_database import SQLDatabaseLoader


def test_run():
    """Test with parametrization."""
    loader = SQLDatabaseLoader("select * from table")
    data = loader.load()

    assert len(data) == 0
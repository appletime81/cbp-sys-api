from schemas import *
from database.models import *
from database.database import get_db_session
from pprint import pprint


def test_query_data():
    db = next(get_db_session())
    data = db.query(InvoiceWKMasterDBModel).all()

    # get data content

    for item in data:
        pprint(item.__dict__)
        print(type(item.__dict__))


if __name__ == "__main__":
    test_query_data()

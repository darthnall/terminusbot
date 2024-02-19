import os
import dotenv
from session import Session

dotenv.load_dotenv()

with Session(token=os.environ['WIALON_HOSTING_API_TOKEN_DEV']) as session:
    print(session.avl_events())

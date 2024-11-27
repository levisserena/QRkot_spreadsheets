from typing import Optional

from pydantic import BaseModel

from app.constants import ConstantGoogle, Text


class GoogleBase(BaseModel):

    name: Optional[str]
    id: Optional[str]
    kind: Optional[str]
    url: Optional[str]
    not_found_table: Optional[str]

    class Config:

        schema_extra = {
            'example': {
                'id': Text.EXAMPLE_ID,
                'kind': 'drive#file',
                'name': f'{Text.TITLE_TABLE_GOOGLE}17:04:52 11/24/24',
                'url': (f'{ConstantGoogle.GET_SPEEEDSHEETS_URL}'
                        f'{Text.EXAMPLE_ID}'),
            }
        }

from typing import Annotated, Union

from fastapi.params import Form
from pydantic import BaseModel, Field


class ObservableSchema(BaseModel):
    type: str = Field(..., min_length=2)
    value: str = Field(..., min_length=3)

    model_config = {
        "json_schema_extra": {"examples": [{"type": "hostname", "value": "cisco.com"}]}
    }


class ActionFormParamsSchema(BaseModel):
    action_id: str = Field(..., alias="action-id", min_length=1)
    observable_type: str = Field(..., min_length=2)
    observable_value: str = Field(..., min_length=3)

    # TODO: Not sure about that:
    # class Meta:
    #     unknown = INCLUDE

    model_config = {"extra": "allow"}


class OAuth2RequestForm:
    def __init__(
        self,
        *,
        grant_type: Annotated[Union[str, None], Form(pattern="password")] = None,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()] = None,
        scope: Annotated[str, Form()] = "",
        client_id: Annotated[Union[str, None], Form()] = None,
        client_secret: Annotated[Union[str, None], Form()] = None,
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

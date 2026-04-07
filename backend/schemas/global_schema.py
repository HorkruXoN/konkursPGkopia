from pydantic import BaseModel, Field
from typing import Optional

# AUTH
class DefReq(BaseModel):
    token: str = Field(..., title="Token", description="Token użytkownika")
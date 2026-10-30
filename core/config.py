from __future__ import annotations
from typing import (
    Final
)
from pydantic import (
    Field,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class Settings(BaseSettings):
    # Required fields
    motion_camera_url: str = Field(
        ...,
        description = "Camera stream address."
    )
    user_name: str = Field(
        ...,
        description = "Login username."
    )
    user_pwd: str = Field(
        ...,
        description = "Login password."
    )

    # Optional fields
    port: int = Field(
        default=8219,
        description="Service port."
    )
    chunk_size: int = Field(
        default=8192,
        description="Data size read each time, in bytes."
    )

    model_config = SettingsConfigDict(
        env_file=[".env", ],
        env_file_encoding="utf-8",
        extra="ignore", # ignore undefined environment variables

        case_sensitive=True,
    )
    
settings: Final[Settings] = Settings() # type: ignore[reportCallIssue]

"""Settings, statically set or loaded and inferred from via environment variables."""
import os
from functools import cached_property
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSingleton(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.dev", ".env.prod"), env_file_encoding="utf-8"
    )

    py_env: Literal["development", "production"]

    def __new__(cls):
        # force this class to be a singleton, for places where do access it outside of
        # blacksheep's dependency injection (where it is already used as one)
        if not hasattr(cls, "_instance"):
            cls._instance = super(EnvironmentSingleton, cls).__new__(cls)

        return cls._instance

    @cached_property
    def is_development(self):
        return self.py_env == "development"

    @cached_property
    def is_production(self):
        return self.py_env == "production"


class ServerSettings:
    accesslog: str = "-"
    worker_class: str = "trio"

    if EnvironmentSingleton().is_development:
        debug: bool = True
        loglevel: str = "DEBUG"
        use_reloader: bool = True
    else:
        try:
            # the number of CPUs the process (server) can access. this may be less than
            # the physical number of (hyperthreaded) cores available.
            workers: int = len(os.sched_getaffinity(0))
        except AttributeError:
            # non-unix environments don't support scheduler affinities
            workers: int = os.cpu_count()

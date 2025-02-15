from pathlib import Path
from typing import TypeVar, MutableMapping
from abc import ABC

BaseRepository = MutableMapping[str | Path, str]

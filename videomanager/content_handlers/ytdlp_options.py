from typing import Callable
from dataclasses import dataclass


@dataclass
class YdlDownloadOptions:
    trigger_string: list[str]
    trigger_callback: Callable
    ytdlp_hook: Callable
    download_path: str
    track_with_ytdlp_archive: bool = True


@dataclass
class YdlInfoOptions:
    pass

import os
import shutil
import subprocess
from difflib import SequenceMatcher
from pathlib import Path


from .config import settings




def ensure_tmp_dir() -> Path:
    p = Path(settings.TEMP_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p




def similarity_score(a: str, b: str) -> int:
    return int(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100)




def convert_webm_to_wav(webm_path: str, wav_path: str) -> None:
# Uses ffmpeg (must be installed on the host)
    cmd = [
    "ffmpeg",
    "-y",
    "-i",
    webm_path,
    "-ar",
    "16000",
    "-ac",
    "1",
    wav_path,
    ]
    subprocess.run(cmd, check=True)




def cleanup_file(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass
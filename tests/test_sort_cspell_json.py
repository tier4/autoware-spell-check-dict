from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from pre_commit_hooks import sort_cspell_json


def test(datadir: Path):
    input_file = datadir / ".cspell.input.json"
    answer_file = datadir / ".cspell.answer.json"

    # Create a temporary file to prevent overwriting original files
    tmp_file = Path(NamedTemporaryFile(mode="w", suffix=".json").name)
    shutil.copy(input_file, tmp_file)

    # Format
    return_code = sort_cspell_json.main([str(tmp_file)])
    assert return_code == 1
    assert tmp_file.read_text() == answer_file.read_text()

    # Re-format
    return_code = sort_cspell_json.main([str(tmp_file)])
    assert return_code == 0
    assert tmp_file.read_text() == answer_file.read_text()

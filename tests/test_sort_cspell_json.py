from pathlib import Path
import shutil

from pre_commit_hooks import sort_cspell_json


def test(tmp_path: Path, datadir: Path):
    input_file = datadir / ".cspell.input.json"
    answer_file = datadir / ".cspell.answer.json"

    # Create a temporary file to prevent overwriting original files
    tmp_file = tmp_path / ".cspell.input.json"
    shutil.copy(input_file, tmp_file)

    # Format
    return_code = sort_cspell_json.main([str(tmp_file)])
    assert return_code == 1
    assert tmp_file.read_text() == answer_file.read_text()

    # Re-format
    return_code = sort_cspell_json.main([str(tmp_file)])
    assert return_code == 0
    assert tmp_file.read_text() == answer_file.read_text()

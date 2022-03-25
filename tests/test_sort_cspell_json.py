from pathlib import Path
import shutil

from pre_commit_hooks import sort_cspell_json


def test(datadir: Path):
    input_file = datadir / ".cspell.input.json"
    answer_file = datadir / ".cspell.answer.json"

    # Create a temporary file to prevent overwriting original files
    target_file = input_file.with_suffix(".target")
    shutil.copy(input_file, target_file)

    # Format
    return_code = sort_cspell_json.main([str(target_file)])
    assert return_code == 1
    assert target_file.read_text() == answer_file.read_text()

    # Re-format
    return_code = sort_cspell_json.main([str(target_file)])
    assert return_code == 0
    assert target_file.read_text() == answer_file.read_text()

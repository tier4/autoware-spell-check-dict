from pathlib import Path

from format_cspell_json import format_cspell_json


def test(datadir: Path):
    input_file = datadir / ".cspell.input.json"
    answer_file = datadir / ".cspell.answer.json"

    # Format
    return_code = format_cspell_json.main([str(input_file)])
    assert return_code == 1
    assert input_file.read_text() == answer_file.read_text()

    # Re-format
    return_code = format_cspell_json.main([str(input_file)])
    assert return_code == 0
    assert input_file.read_text() == answer_file.read_text()

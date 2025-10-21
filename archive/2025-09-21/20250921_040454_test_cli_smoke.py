from scripturemon_champion.cli import main
from pathlib import Path
def test_cli_analyze(tmp_path, capsys):
    f = tmp_path / 'roteiro.txt'
    f.write_text('INT. CASA - DIA\nMARIA\nEu te amo.\nEXT. PRAIA - TARDE', encoding='utf-8')
    rc = main(['analyze', str(f)])
    out = capsys.readouterr().out
    assert 'scenes' in out
    assert rc is None or rc == 0

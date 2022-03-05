from .context import dbspan


def test_app(capsys):
    # pylint: disable=W0612,W0613
    dbspan.DBSpan.run()
    captured = capsys.readouterr()
    expected_out = "Hello world"
    assert expected_out in captured.out

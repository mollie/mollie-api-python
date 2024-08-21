from mollie.api.objects.terminal import Terminal

from .utils import assert_list_object

TERMINAL_ID = "term_7MgL4wea46qkRcoTZjWEH"


def test_get_terminal(client, response):
    response.get(f"https://api.mollie.com/v2/terminals/{TERMINAL_ID}", "terminal_single")

    terminal = client.terminals.get(TERMINAL_ID)

    assert terminal.id == TERMINAL_ID


def test_list_terminals(client, response):
    response.get("https://api.mollie.com/v2/terminals", "terminals_list")

    terminals = client.terminals.list()
    assert_list_object(terminals, Terminal)

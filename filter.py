"""Template for firewall filter modules."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from firewall.proxy.stream import HTTPStream, TCPStream


class Module:
    """Template for filter modules."""

    slots = ("_filters",)

    def __init__(self) -> None:
        """Initialize the filter module and pre-load its filter functions."""
        IGNORED = frozenset(("execute",))  # noqa: N806

        self._filters = tuple(
            func
            for name, func in Module.__dict__.items()
            if not name.startswith("_") and name not in IGNORED and callable(func)
        )

    def block_attacker_headers(self, stream):
        import re

        msg = stream.current_http_message
        if msg is None:
            return False

        if msg.method != "GET":
            return False

        if re.fullmatch(r"/view/\d+", msg.path or "") is None:
            return False

        headers = {k.lower(): v for k, v in msg.headers.items()}

        return (
            headers.get("user-agent") == "python-requests/2.28.2"
            and headers.get("accept-encoding") == "identity"
        )

    def execute(self, stream: TCPStream | HTTPStream) -> str | None:
        """
        Execute the filter module, calling all the filter functions
        defined in the module.

        Return
        ------
        str | None :
            A string that identifies the attack name. If None is returned,
            no attack has been identified inside data.
        """
        for attack in self._filters:
            if attack(self, stream):
                return attack.__name__

        return None

    # INFO: Add your filter functions here
    # NOTE: Use slots pattern for filter functions if they store state
"""Embed token definition."""

from types import SimpleNamespace


class EmbedToken(SimpleNamespace):
    """
    A Power BI embed token.

    """

    def __init__(
        self,
        token: str,
        token_id: str,
        expiration: str,
    ):
        super().__init__(
            token=token,
            token_id=token_id,
            expiration=expiration,
        )

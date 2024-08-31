from authlib.integrations.httpx_client import AsyncOAuth1Client, OAuth1Auth


class BlizzardClient:

    auth_url: str = "https://oauth.battle.net/token"

    client: AsyncOAuth1Client
    auth: OAuth1Auth

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.client = AsyncOAuth1Client(self.client_id, self.client_secret)

    async def _get_access_token(self):
        access_token = await self.client.fetch_access_token(self.auth_url)
        # self.auth = OAuth1Auth(
        #     client_id=self.client_id,
        #     client_secret=self.client_secret,
        #     token=access_token[""],
        #     token_secret=access_token[""]
        # )

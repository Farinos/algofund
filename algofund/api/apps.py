from django.apps import AppConfig
from algosdk.v2client.algod import AlgodClient


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    client: AlgodClient = AlgodClient('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'http://localhost:4001')

    def ready(self) -> None:
        return super().ready()
from django.apps import AppConfig
from algosdk.v2client.algod import AlgodClient


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    client: AlgodClient = AlgodClient('token', 'address')

    def ready(self) -> None:
        return super().ready()
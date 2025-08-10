from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_name: str = "greg-mvp"
    app_env: str = "development"
    bigquery_project: str = ""
    okta_issuer_url: str = ""
    okta_audience: str = ""
    
    model_config = {"env_file": ".env"}
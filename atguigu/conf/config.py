from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file= Path(__file__).parents[2] / '.env' ,
        env_file_encoding= 'utf-8',
        extra="ignore"
    )

    llm_model:str
    llm_base_url:str
    llm_api_key:str

    database_url:str
    commerce_api_base_url:str

    app_host:str
    app_port:int


settings = settings()

if __name__ == '__main__':
    print(settings.llm_model)
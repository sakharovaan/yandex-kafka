from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class KafkaConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="PRODUCER_") 

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
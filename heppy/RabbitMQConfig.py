# -*- coding: utf-8 -*-

import json
import os

ENV_OVERRIDES = {
    'username': 'RABBITMQ_USERNAME',
    'password': 'RABBITMQ_PASSWORD',
}

CREDENTIALS_FILE_ENV = 'RABBITMQ_CREDENTIALS_FILE'


class RabbitMQConfig:
    """Resolves the final RabbitMQ.* config dict for a worker: config file
    values, the default queue name, and a RabbitMQ.username/password
    override from either RABBITMQ_USERNAME/RABBITMQ_PASSWORD env vars or a
    single RABBITMQ_CREDENTIALS_FILE pointing at a JSON file shaped
    {"username": ..., "password": ...} -- matching how the credential pair
    is already kept together as one Kubernetes Secret (ahnames-epp-rabbitmq)
    rather than two, so that Secret can be mounted as one file and read as
    one unit instead of two separately-sourced values.

    Exactly one of the two sources may be used at a time -- setting
    RABBITMQ_CREDENTIALS_FILE together with either plain env var is
    rejected outright rather than picking one silently. Within either
    source, an override is applied whenever its value is *present*, even an
    empty string, so it can't be silently mistaken for "unset" and fall
    back to a stale config value.

    A deployment injects these from the same secret the broker itself
    reads, so a credential rotation only needs that one secret updated
    instead of resealing every worker's config file to match a copy of the
    password."""

    def __init__(self, config):
        self.config = config

    def resolve(self):
        rabbit_config = self._config_section()
        rabbit_config.setdefault('queue', 'heppy-' + self.config['name'])

        has_file = CREDENTIALS_FILE_ENV in os.environ
        has_plain = any(env_name in os.environ for env_name in ENV_OVERRIDES.values())
        if has_file and has_plain:
            plain_names = ' / '.join(ENV_OVERRIDES.values())
            raise ValueError(f"both {CREDENTIALS_FILE_ENV} and {plain_names} are set - pick one")

        if has_file:
            with open(os.environ[CREDENTIALS_FILE_ENV]) as f:
                credentials = json.load(f)
            for key in ENV_OVERRIDES:
                if key in credentials:
                    rabbit_config[key] = credentials[key]
        else:
            for key, env_name in ENV_OVERRIDES.items():
                if env_name in os.environ:
                    rabbit_config[key] = os.environ[env_name]

        return rabbit_config

    def _config_section(self):
        if 'RabbitMQ' in self.config:
            return dict(self.config['RabbitMQ'])
        return {}

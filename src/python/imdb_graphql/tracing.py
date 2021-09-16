import logging
import yaml

from jaeger_client import Config


def get_tracer():
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    with open('tracer_cfg.yaml') as cf:
        tracer_cfg = yaml.load(cf.read())

    config = Config(
        config=tracer_cfg,
        service_name='imdb',
        validate=True,
    )
    return config.initialize_tracer()

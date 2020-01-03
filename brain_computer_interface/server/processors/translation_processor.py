import json

from .processor import Processor
from ..server import Server, TIMESTAMP, POSE


@Server.processor(TIMESTAMP, POSE)
class TranslationProcessor(Processor):
    def process(self, snapshot):
        translation = snapshot[POSE]['translation']
        with open(self.get_dir(snapshot[TIMESTAMP]) / 'translation.json', 'w+') as f:
            json.dump(translation, f)

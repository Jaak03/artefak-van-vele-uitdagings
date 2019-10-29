import json

if __name__ == "__main__":
    import sys, os
    sys.path.append( os.getcwd() )

from base.message_bucket import TestMessage
from base.console_message import comment, error


class FeatureJSON:
    def __init__(self):
        self.author = ""
        self.features = []
        self.word_count = 0
        self.words = []
    
    def __str__(self):
        tmp2write = {}
        tmp2write["author"] = self.author
        tmp2write["features"] = self.features
        tmp2write["word_count"] = self.word_count
        tmp2write["words"] = self.words

        return str(json.dumps(tmp2write))

class HandleJSON:
    def __init__(self, path: str):
        comment(f"Handling JSON entry for {path}.")

HandleJSON('iets')
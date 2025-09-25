import json
import logging as _logging
import re
from pprint import pformat


class LoggerException(Exception):
    pass


class PrettyEmbeddedJSONFormatter(_logging.Formatter):
    json_regex = re.compile(r'(\{.*}|\[.*])')  # crude but works for simple dict/list

    def format(self, record):
        msg = record.getMessage()

        # Find all JSON/dict-like substrings
        def pretty_sub(match):
            text = match.group(0)
            try:
                parsed = json.loads(text.replace("'", "\""))
                return json.dumps(parsed, indent=4)
            except json.JSONDecodeError:
                # If it's Python-style dict, use eval cautiously
                try:
                    parsed = eval(text, {"__builtins__": None}, {})
                    if isinstance(parsed, (dict, list)):
                        return pformat(parsed, indent=4)
                except LoggerException:
                    pass
            return text

        pretty_msg = self.json_regex.sub(pretty_sub, msg)
        record.msg = pretty_msg
        record.args = ()
        return super().format(record)


class Log:
    def __init__(self, name=__name__, pretty_format=False):
        self.name = name
        self.pretty_format = pretty_format
        if "." in name:
            self.logger = _logging.getLogger(name=self.name.split(".")[0]).getChild(".".join(self.name.split(".")[1:]))
        else:
            self.logger = _logging.getLogger(name=self.name)

    def set_handler(
            self,
            level="warn",
            formatter="%(asctime)s - %(name)s - %(levelname)s \t %(message)s",
    ):
        """<type_>: "Critical"/ "Error" / "Warning"/ "Info"/ "Debug" """

        if self.pretty_format:
            _formatter = PrettyEmbeddedJSONFormatter(formatter)
        else:
            _formatter = _logging.Formatter(formatter)
        _handler = _logging.StreamHandler()

        if level.lower().startswith("c"):
            _handler.setLevel(_logging.CRITICAL)
            level_to_set = "CRITICAL"

        elif level.lower().startswith("e"):
            _handler.setLevel(_logging.ERROR)
            level_to_set = "ERROR"

        elif level.lower().startswith("w"):
            _handler.setLevel(_logging.WARNING)
            level_to_set = "WARNING"

        elif level.lower().startswith("d"):
            _handler.setLevel(_logging.DEBUG)
            level_to_set = "DEBUG"

        else:
            _handler.setLevel(_logging.INFO)
            level_to_set = "INFO"

        _handler.setFormatter(_formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(_handler)
            self.logger.setLevel(level_to_set)
            self.logger.propagate = False
        else:
            handler_list = [str(x).strip("<>").split("stderr")[1].strip(" ()") for x in self.logger.handlers]
            if level_to_set not in handler_list:
                self.logger.addHandler(_handler)
                self.logger.setLevel(level_to_set)
                self.logger.propagate = False


def loggers():
    logger = {}
    for level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "LOCKS"]:
        logger[level] = Log(name="CLASSES." + level)
        logger[level].set_handler(
            level=level if level != "LOCKS" else "INFO",
            formatter=(
                "[%(asctime)s]: %(lineno)d | %(module)s | %(thread)d - %(threadName)s | {}"
                "\t \n\n%(message)s\n\n".format(level if level != "LOCKS" else "INFO")
            ),
        )
    return logger

import logging as _logging


class Log:
    def __init__(self, name=__name__):
        self.name = name
        if "." in name:
            self.logger = _logging.getLogger(name=self.name.split(".")[0]).getChild(
                ".".join(self.name.split(".")[1:])
            )
        else:
            self.logger = _logging.getLogger(name=self.name)

    def set_handler(
        self,
        level="warn",
        formatter="%(asctime)s - %(name)s - %(levelname)s \t %(message)s",
    ):
        """<type_>: "Critical"/ "Error" / "Warning"/ "Info"/ "Debug" """

        if level.lower().startswith("c"):
            _handler = _logging.StreamHandler()
            _handler.setLevel(_logging.CRITICAL)
            _handler.setFormatter(_logging.Formatter(formatter))
            if not self.logger.hasHandlers():
                self.logger.addHandler(_handler)
                self.logger.setLevel("CRITICAL")
                self.logger.propagate = False
            else:
                handler_list = [
                    str(x).strip("<>").split("stderr")[1].strip(" ()")
                    for x in self.logger.handlers
                ]
                if "CRITICAL" not in handler_list:
                    self.logger.addHandler(_handler)
                    self.logger.setLevel("CRITICAL")
                    self.logger.propagate = False

        elif level.lower().startswith("e"):
            _handler = _logging.StreamHandler()
            _handler.setLevel(_logging.ERROR)
            _handler.setFormatter(_logging.Formatter(formatter))
            if not self.logger.hasHandlers():
                self.logger.addHandler(_handler)
                self.logger.setLevel("ERROR")
                self.logger.propagate = False
            else:
                handler_list = [
                    str(x).strip("<>").split("stderr")[1].strip(" ()")
                    for x in self.logger.handlers
                ]
                if "ERROR" not in handler_list:
                    self.logger.addHandler(_handler)
                    self.logger.setLevel("ERROR")
                    self.logger.propagate = False

        elif level.lower().startswith("w"):
            _handler = _logging.StreamHandler()
            _handler.setLevel(_logging.WARNING)
            _handler.setFormatter(_logging.Formatter(formatter))
            if not self.logger.hasHandlers():
                self.logger.addHandler(_handler)
                self.logger.setLevel("WARNING")
                self.logger.propagate = False
            else:
                handler_list = [
                    str(x).strip("<>").split("stderr")[1].strip(" ()")
                    for x in self.logger.handlers
                ]
                if "WARNING" not in handler_list:
                    self.logger.addHandler(_handler)
                    self.logger.setLevel("WARNING")
                    self.logger.propagate = False

        elif level.lower().startswith("i"):
            _handler = _logging.StreamHandler()
            _handler.setLevel(_logging.INFO)
            _handler.setFormatter(_logging.Formatter(formatter))
            if not self.logger.hasHandlers():
                self.logger.addHandler(_handler)
                self.logger.setLevel("INFO")
                self.logger.propagate = False

            else:
                handler_list = [
                    str(x).strip("<>").split("stderr")[1].strip(" ()")
                    for x in self.logger.handlers
                ]
                if "INFO" not in handler_list:
                    self.logger.addHandler(_handler)
                    self.logger.setLevel("INFO")
                    self.logger.propagate = False

        elif level.lower().startswith("d"):
            _handler = _logging.StreamHandler()
            _handler.setLevel(_logging.DEBUG)
            _handler.setFormatter(_logging.Formatter(formatter))
            if not self.logger.hasHandlers():
                self.logger.addHandler(_handler)
                self.logger.setLevel("DEBUG")
                self.logger.propagate = False
            else:
                handler_list = [
                    str(x).strip("<>").split("stderr")[1].strip(" ()")
                    for x in self.logger.handlers
                ]
                if "DEBUG" not in handler_list:
                    self.logger.addHandler(_handler)
                    self.logger.setLevel("DEBUG")
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

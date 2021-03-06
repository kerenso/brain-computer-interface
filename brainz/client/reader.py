from .mind import SampleParser, BinaryParser, ProtobufParser, ParsingError
from ..protocol.fields import USER_ID


def _get_parser(protobuf: bool) -> SampleParser:
    """
    :param protobuf: Whether to return the protobuf parser.
    :return: The relevant parser according to `protobuf`.
    """
    if protobuf:
        return ProtobufParser()
    return BinaryParser()


class Reader:
    """
    A reader used to extracting user information and snapshots from sample files.
    """

    def __init__(self, file_path: str, protobuf: bool) -> None:
        """
        Parse the user from the given sample and initiate the data members of the class.

        :param file_path: The path to the sample file.
        :param protobuf: Whether to use a protobuf or binary format.
        """
        self.parser = _get_parser(protobuf)
        self.file = self.parser.open(file_path, "rb")
        self.user = self.parser.parse_user(self.file)

        self.user[USER_ID] = int(self.user[USER_ID])

    def __iter__(self):
        """
        Iterate over and parse the snapshots in the sample file.
        """
        while True:
            try:
                s = self.parser.parse_snapshot(self.file)
            except ParsingError:
                self.file.close()
                break
            yield s

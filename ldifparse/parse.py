import sys
from ldif import LDIFParser


class Parser(LDIFParser):
    def __init__(
        self,
        input_file,
        dump_method,
        ignored_attr_types=None,
        max_entries=0,
        process_url_schemes=None,
        line_sep="\n",
    ):
        super().__init__(
            input_file, ignored_attr_types, max_entries, process_url_schemes, line_sep
        )

        self.data = {}
        self.dump_method = dump_method

    def print(self) -> None:
        self.dump_method(self.data, sys.stdout)


class Parser_base(Parser):
    def handle(self, dn: str, entry: dict[str, list[bytes]]):
        self.data[dn] = {}

        for k, v in entry.items():
            decoded_values = []
            for value in v:
                try:
                    decoded_values.append(value.decode("utf-8"))
                except UnicodeDecodeError:
                    decoded_values.append(str(value))

            if len(decoded_values) == 1:
                self.data[dn][k] = decoded_values[0]

            elif len(decoded_values) >= 1:
                self.data[dn][k] = decoded_values


class Parser_tree(Parser):
    def handle(self, dn: str, entry: dict[str, list[bytes]]):
        data_store = self.data

        for key in reversed(dn.split(",")):
            if len(key.split("=")) > 1:
                data_store = data_store.setdefault("_".join(key.split("=")), {})

            else:
                data_store = data_store.setdefault(key, {})

        for k, v in entry.items():
            decoded_values = []
            for value in v:
                try:
                    decoded_values.append(value.decode("utf-8"))
                except UnicodeDecodeError:
                    decoded_values.append(str(value))

            if len(decoded_values) == 1:
                data_store[k] = decoded_values[0]

            elif len(decoded_values) >= 1:
                data_store[k] = decoded_values

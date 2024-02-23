import sys
import yaml
from ldif import LDIFParser


class LDIF2YAML(LDIFParser):
    def __init__(
        self,
        input_file,
        ignored_attr_types=None,
        max_entries=0,
        process_url_schemes=None,
        line_sep="\n",
    ):
        super().__init__(
            input_file, ignored_attr_types, max_entries, process_url_schemes, line_sep
        )

        self.data = {}

    def print(self) -> None:
        yaml.dump(self.data, sys.stdout)


class LDIF2YAML_base(LDIF2YAML):
    def handle(self, dn: str, entry: dict[str, list[bytes]]):
        self.data[dn] = {}

        for k, v in entry.items():
            decoded_values = []
            for value in v:
                try:
                    decoded_values.append(value.decode("utf-8"))
                except UnicodeDecodeError:
                    decoded_values.append(value)

            if len(decoded_values) == 1:
                self.data[dn][k] = decoded_values[0]

            elif len(decoded_values) >= 1:
                self.data[dn][k] = decoded_values


class LDIF2YAML_tree(LDIF2YAML):
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
                    decoded_values.append(value)

            if len(decoded_values) == 1:
                data_store[k] = decoded_values[0]

            elif len(decoded_values) >= 1:
                data_store[k] = decoded_values

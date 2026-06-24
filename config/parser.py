import sys
import json


class Parser:
    def parse_arguments(self) -> bool:
        if len(sys.argv) != 2:
            print("Wrong number of arguments")
            return False
        elif not sys.argv[1].endswith(".json"):
            print("It must be a .json file")
            return False
        return True

    def get_file(self) -> str:
        file = sys.argv[1]
        return file

    def open_file(self, file: str) -> None | str:
        try:
            with open(file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception("File not found")

    def format_file(self, file: str) -> str:
        lines = [line for line in file.splitlines() if not line.startswith("#")]
        return '\n'.join(lines)

    def read_file(self, file: str) -> None | dict:
        try:
            fields = json.loads(file)
            return fields
        except json.JSONDecodeError as e:
            raise Exception("Invalid JSON syntax:", e)

    def run_parsing(self) -> dict:
        if self.parse_arguments():
            try:
                file = self.get_file()
                result = self.open_file(file)
                new_result = self.format_file(result)
                end_file = self.read_file(new_result)
                return end_file
            except Exception as e:
                print(e)
        else:
            return


if __name__ == '__main__':
    parsing = Parser()
    parsing.run_parsing()

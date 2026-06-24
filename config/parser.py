import sys
import json


class Parser:

    DEFAULTS = {
        "highscore_filename": "highscores.json",
        "lives": 3,
        "seed": 42,
        "level_max_time": 90,
        "pacgum": 10,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "levels": [
            {"width": 15, "height": 11},
            {"width": 17, "height": 13},
            {"width": 19, "height": 15},
            {"width": 21, "height": 15},
            {"width": 23, "height": 17},
            {"width": 25, "height": 17},
            {"width": 25, "height": 19},
            {"width": 27, "height": 19},
            {"width": 29, "height": 21},
            {"width": 31, "height": 21}
            ]
    }

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
        lines = [line for line in 
                 file.splitlines() if not line.strip().startswith("#")]
        return '\n'.join(lines)

    def read_file(self, file: str) -> None | dict:
        try:
            fields = json.loads(file)
            return fields
        except json.JSONDecodeError as e:
            raise Exception("Invalid JSON syntax:", e)

    def parse_keys(self, file: dict) -> dict:
        result = {**self.DEFAULTS, **file}

        if not result["highscore_filename"].endswith(".json"):
            result["highscore_filename"] = self.DEFAULTS["highscore_filename"]

        if not isinstance(result["lives"], int) or result["lives"] < 1:
            result["lives"] = self.DEFAULTS["lives"]

        for i, level in enumerate(result["levels"]):
            if i < len(self.DEFAULTS["levels"]):
                if not isinstance(level["width"], int) or level["width"] < 1:
                    level["width"] = self.DEFAULTS["levels"][i]["width"]
                if not isinstance(level["height"], int) or level["height"] < 1:
                    level["height"] = self.DEFAULTS["levels"][i]["height"]

        if not isinstance(result["pacgum"], int) or result["pacgum"] < 1:
            result["pacgum"] = self.DEFAULTS["pacgum"]

        if not isinstance(result["points_per_pacgum"], int) or result["points_per_pacgum"] < 1:
            result["points_per_pacgum"] = self.DEFAULTS["points_per_pacgum"]

        if not isinstance(result["points_per_super_pacgum"], int) or result["points_per_super_pacgum"] < 1:
            result["points_per_super_pacgum"] = self.DEFAULTS["points_per_super_pacgum"]

        if not isinstance(result["points_per_ghost"], int) or result["points_per_ghost"] < 1:
            result["points_per_ghost"] = self.DEFAULTS["points_per_ghost"]

        if not isinstance(result["seed"], int) or result["seed"] < 1:
            result["seed"] = self.DEFAULTS["seed"]

        if not isinstance(result["level_max_time"], int) or result["level_max_time"] < 1:
            result["level_max_time"] = self.DEFAULTS["level_max_time"]

        return result

    def run_parsing(self) -> None | dict:
        if self.parse_arguments():
            try:
                file = self.get_file()
                result = self.open_file(file)
                new_result = self.format_file(result)
                end_file = self.read_file(new_result)
                keys = self.parse_keys(end_file)
                return keys
            except Exception as e:
                print(e)
        else:
            return


if __name__ == '__main__':
    parsing = Parser()
    print(parsing.run_parsing())

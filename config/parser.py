import sys
import json
from typing import Any, ClassVar, Optional

from contracts import GameConfig


class Parser:
    """Parses command-line arguments and a JSON config file into a GameConfig.

    Handles argument validation, file reading, comment stripping, JSON parsing,
    field validation with fallback to defaults, and final conversion to a typed
    GameConfig dataclass.
    """

    DEFAULTS: ClassVar[dict[str, Any]] = {
        "highscore_filename": "highscores.json",
        "lives": 3,
        "seed": 42,
        "level_max_time": 90,
        "pacgum": 10,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "ghost_respawn_time": 5.0,
        "ghost_flee_time": 7.0,
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
            {"width": 31, "height": 21},
        ],
    }

    def parse_arguments(self) -> bool:
        """Validate that exactly one argument is provided and it is a
        .json file.

        Returns:
            True if the arguments are valid, False otherwise.
        """
        if len(sys.argv) != 2:
            print("Wrong number of arguments")
            return False
        if not sys.argv[1].endswith(".json"):
            print("It must be a .json file")
            return False
        return True

    def get_file(self) -> str:
        """Return the file path passed as the first command-line argument.

        Returns:
            The file path string from sys.argv[1].
        """
        return sys.argv[1]

    def open_file(self, file: str) -> str:
        """Read and return the raw contents of the given file.

        Args:
            file: Path to the file to open.

        Returns:
            The full contents of the file as a string.

        Raises:
            Exception: If the file is not found.
        """
        try:
            with open(file, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise Exception("File not found")

    def format_file(self, file: str) -> str:
        """Strip comment lines (starting with '#') from the file contents.

        Args:
            file: Raw file contents as a string.

        Returns:
            The file contents with comment lines removed.
        """
        lines: list[str] = [
            line for line in file.splitlines()
            if not line.strip().startswith("#")
        ]
        return "\n".join(lines)

    def read_file(self, file: str) -> dict[str, Any]:
        """Parse a JSON string into a dictionary.

        Args:
            file: A string containing valid JSON.

        Returns:
            The parsed JSON data as a dictionary.

        Raises:
            Exception: If the string is not valid JSON.
        """
        try:
            fields: dict[str, Any] = json.loads(file)
            return fields
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON syntax: {e}")

    def parse_keys(self, file: dict[str, Any]) -> dict[str, Any]:
        """Merge the provided config with defaults and validate each field.

        Unknown keys are kept; invalid values are replaced with their defaults.

        Args:
            file: Parsed JSON config as a dictionary.

        Returns:
            A dictionary with all required keys present and validated.
        """
        result: dict[str, Any] = {**self.DEFAULTS, **file}

        if not isinstance(result["highscore_filename"], str) or \
                not result["highscore_filename"].endswith(".json"):
            result["highscore_filename"] = self.DEFAULTS["highscore_filename"]

        if not isinstance(result["lives"], int) or result["lives"] < 1:
            result["lives"] = self.DEFAULTS["lives"]

        for i, level in enumerate(result["levels"]):
            if i < len(self.DEFAULTS["levels"]):
                if not isinstance(level["width"], int) or level["width"] < 1:
                    level["width"] = self.DEFAULTS["levels"][i]["width"]
                if not isinstance(level["height"], int) or level["height"] < 1:
                    level["height"] = self.DEFAULTS["levels"][i]["height"]

        if not isinstance(result["pacgum"], int) or \
                result["pacgum"] < 1:
            result["pacgum"] = self.DEFAULTS["pacgum"]

        if not isinstance(result["points_per_pacgum"], int) or \
                result["points_per_pacgum"] < 1:
            result["points_per_pacgum"] = self.DEFAULTS["points_per_pacgum"]

        if not isinstance(result["points_per_super_pacgum"], int) or \
                result["points_per_super_pacgum"] < 1:
            result["points_per_super_pacgum"] = \
                self.DEFAULTS["points_per_super_pacgum"]

        if not isinstance(result["points_per_ghost"], int) or \
                result["points_per_ghost"] < 1:
            result["points_per_ghost"] = self.DEFAULTS["points_per_ghost"]

        if not isinstance(result["seed"], int) or result["seed"] < 1:
            result["seed"] = self.DEFAULTS["seed"]

        if not isinstance(result["level_max_time"], int) or \
                result["level_max_time"] < 1:
            result["level_max_time"] = self.DEFAULTS["level_max_time"]

        if not isinstance(result["ghost_respawn_time"], float) or \
                result["ghost_respawn_time"] < 1:
            result["ghost_respawn_time"] = self.DEFAULTS["ghost_respawn_time"]

        if not isinstance(result["ghost_flee_time"], float) or \
                result["ghost_flee_time"] < 1:
            result["ghost_flee_time"] = self.DEFAULTS["ghost_flee_time"]

        return result

    def to_game_config(self, result: dict[str, Any]) -> GameConfig:
        """Convert a validated config dictionary into a GameConfig instance.

        Args:
            result: A fully validated config dictionary from parse_keys.

        Returns:
            A GameConfig dataclass populated with the config values.
        """
        levels_as_tuples: list[tuple[int, int]] = [
            (level["width"], level["height"])
            for level in result["levels"]
        ]

        return GameConfig(
            levels=levels_as_tuples,
            lives=result["lives"],
            pacgum=result["pacgum"],
            points_per_pacgum=result["points_per_pacgum"],
            points_per_super_pacgum=result["points_per_super_pacgum"],
            points_per_ghost=result["points_per_ghost"],
            ghost_respawn_time=result["ghost_respawn_time"],
            ghost_flee_time=result["ghost_flee_time"],
            level_max_time=result["level_max_time"],
            seed=result["seed"],
            highscore_filename=result["highscore_filename"],
        )

    def run_parsing(self) -> Optional[GameConfig]:
        """Run the full parsing pipeline and return the resulting GameConfig.

        Validates arguments, reads and parses the config file, applies
        defaults, and builds a GameConfig. Prints any errors encountered.

        Returns:
            A GameConfig on success, or None if arguments are invalid or an
            error occurs during parsing.
        """
        if not self.parse_arguments():
            return None
        try:
            file: str = self.get_file()
            raw: str = self.open_file(file)
            formatted: str = self.format_file(raw)
            fields: dict[str, Any] = self.read_file(formatted)
            keys: dict[str, Any] = self.parse_keys(fields)
            return self.to_game_config(keys)
        except Exception as e:
            print(e)
            return None

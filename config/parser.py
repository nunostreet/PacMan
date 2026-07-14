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
            raise Exception(f"File not found: {file}")
        except PermissionError:
            raise Exception(f"Permission denied: {file}")

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
            data: Any = json.loads(file)
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON syntax: {e}")
        if not isinstance(data, dict):
            raise Exception("Config file must be a JSON object, not an array")
        fields: dict[str, Any] = data
        return fields

    @staticmethod
    def _clamp(
            value: Any,
            t: type | tuple[type, ...],
            min_val: Any,
            default: Any
            ) -> Any:
        """Return value if it matches type t and >= min_val, else default."""
        if not isinstance(value, t) or value < min_val:
            return default
        return value

    def parse_keys(self, file: dict[str, Any]) -> dict[str, Any]:
        """Merge the provided config with defaults and validate each field.

        Unknown keys are kept; invalid values are replaced with their defaults.

        Args:
            file: Parsed JSON config as a dictionary.

        Returns:
            A dictionary with all required keys present and validated.
        """
        result: dict[str, Any] = {**self.DEFAULTS, **file}
        D = self.DEFAULTS

        if not isinstance(result["highscore_filename"], str) or \
                not result["highscore_filename"].endswith(".json"):
            result["highscore_filename"] = D["highscore_filename"]

        result["lives"] = self._clamp(result["lives"], int, 1, D["lives"])
        result["seed"] = self._clamp(result["seed"], int, 1, D["seed"])
        result["level_max_time"] = self._clamp(
            result["level_max_time"], int, 1, D["level_max_time"]
        )
        result["pacgum"] = self._clamp(result["pacgum"], int, 1, D["pacgum"])
        result["points_per_pacgum"] = self._clamp(
            result["points_per_pacgum"], int, 1, D["points_per_pacgum"]
        )
        result["points_per_super_pacgum"] = self._clamp(
            result["points_per_super_pacgum"],
            int, 1, D["points_per_super_pacgum"]
        )
        result["points_per_ghost"] = self._clamp(
            result["points_per_ghost"], int, 1, D["points_per_ghost"]
        )
        result["ghost_respawn_time"] = float(self._clamp(
            result["ghost_respawn_time"], (int, float), 1,
            D["ghost_respawn_time"]
        ))
        result["ghost_flee_time"] = float(self._clamp(
            result["ghost_flee_time"], (int, float), 1, D["ghost_flee_time"]
        ))

        if not isinstance(result["levels"], list) or \
                len(result["levels"]) < 1:
            result["levels"] = D["levels"]

        for i, level in enumerate(result["levels"]):
            fallback = D["levels"][min(i, len(D["levels"]) - 1)]
            if not isinstance(level, dict):
                result["levels"][i] = fallback
                continue
            level["width"] = self._clamp(
                level.get("width"), int, 1, fallback["width"]
            )
            level["height"] = self._clamp(
                level.get("height"), int, 1, fallback["height"]
            )

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

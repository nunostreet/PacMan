from engine.player import Pacman
from contracts import Direction


def test_init():
    pacman = Pacman(start_x=7, start_y=5, lives=3)
    assert pacman.x == 7
    assert pacman.y == 5
    assert pacman.lives == 3


def test_respawn():
    pacman = Pacman(start_x=7, start_y=5, lives=3)
    pacman.respawn(7, 5)
    assert pacman.lives == 2
    assert pacman.x == 7
    assert pacman.y == 5


neighbors = {
    (0, 0): [(1, 0), (0, 1)],
    (1, 0): [(0, 0)],
    (0, 1): [(0, 0)],
}


def test_move_valid():
    pacman = Pacman(0, 0, 3)
    result = pacman.move(Direction.RIGHT, neighbors)
    assert result
    assert pacman.x == 1
    assert pacman.y == 0


def test_move_blocked():
    pacman = Pacman(0, 0, 3)
    result = pacman.move(Direction.UP, neighbors)
    assert not result
    assert pacman.x == 0
    assert pacman.y == 0

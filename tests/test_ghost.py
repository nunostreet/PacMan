from engine.ghost import Ghost

# Simple linear corridor: (0,0) - (1,0) - (2,0)
LINEAR: dict[tuple[int, int], list[tuple[int, int]]] = {
    (0, 0): [(1, 0)],
    (1, 0): [(0, 0), (2, 0)],
    (2, 0): [(1, 0)],
}

# T-junction: (1,0) connects left, right, and down
T_JUNCTION: dict[tuple[int, int], list[tuple[int, int]]] = {
    (0, 0): [(1, 0)],
    (1, 0): [(0, 0), (2, 0), (1, 1)],
    (2, 0): [(1, 0)],
    (1, 1): [(1, 0)],
}


# ── no-reverse rule ──────────────────────────────────────────────────────────

def test_no_reverse_in_corridor() -> None:
    ghost = Ghost(0, 0)
    ghost.move(LINEAR, (2, 0))
    assert (ghost.x, ghost.y) == (1, 0)
    ghost.move(LINEAR, (2, 0))
    assert (ghost.x, ghost.y) == (2, 0)


def test_no_reverse_allows_backtrack_when_only_option() -> None:
    ghost = Ghost(1, 0)
    ghost.move(LINEAR, (0, 0))
    pos = (ghost.x, ghost.y)
    assert pos in [(0, 0), (2, 0)]
    ghost.move(LINEAR, (0, 0))
    # if ghost went to (2,0), only option back is (1,0) — allowed
    assert (ghost.x, ghost.y) == (1, 0)


# ── chase mode ───────────────────────────────────────────────────────────────

def test_chase_moves_toward_pacman() -> None:
    ghost = Ghost(0, 0)
    ghost.move(T_JUNCTION, (2, 0))
    assert (ghost.x, ghost.y) == (1, 0)
    ghost.move(T_JUNCTION, (2, 0))
    assert (ghost.x, ghost.y) == (2, 0)


def test_chase_does_not_move_when_respawning() -> None:
    ghost = Ghost(1, 0)
    ghost.respawn_timer = 3.0
    ghost.move(LINEAR, (2, 0))
    assert (ghost.x, ghost.y) == (1, 0)


# ── scatter mode ─────────────────────────────────────────────────────────────

def test_scatter_targets_spawn_corner() -> None:
    ghost = Ghost(2, 0)
    ghost.move(LINEAR, (99, 99), scatter=True)
    assert (ghost.x, ghost.y) == (1, 0)


# ── flee mode ────────────────────────────────────────────────────────────────

def test_flee_moves_away_from_pacman() -> None:
    ghost = Ghost(1, 0)
    ghost.edible = True
    ghost.flee_timer = 5.0
    # pacman at (0,0) — fleeing should prefer (2,0)
    outcomes = set()
    for _ in range(20):
        g = Ghost(1, 0)
        g.edible = True
        g.flee_timer = 5.0
        g.move(LINEAR, (0, 0))
        outcomes.add((g.x, g.y))
    # (2,0) must appear (it's the furthest); (0,0) may appear due to noise
    assert (2, 0) in outcomes


# ── timers ───────────────────────────────────────────────────────────────────

def test_flee_timer_expires_and_clears_edible() -> None:
    ghost = Ghost(0, 0)
    ghost.edible = True
    ghost.flee_timer = 0.1
    ghost.update(0.2)
    assert not ghost.edible
    assert ghost.flee_timer == 0.0


def test_flee_timer_does_not_go_negative() -> None:
    ghost = Ghost(0, 0)
    ghost.edible = True
    ghost.flee_timer = 0.05
    ghost.update(1.0)
    assert ghost.flee_timer == 0.0


def test_respawn_timer_returns_ghost_to_start() -> None:
    ghost = Ghost(3, 3)
    ghost.respawn(0.1)
    assert ghost.respawn_timer > 0
    ghost.update(0.2)
    assert ghost.respawn_timer == 0.0
    assert ghost.x == 3
    assert ghost.y == 3


def test_respawn_clears_edible_and_prev() -> None:
    ghost = Ghost(0, 0)
    ghost.edible = True
    ghost._prev = (1, 0)
    ghost.respawn(5.0)
    assert not ghost.edible
    assert ghost._prev is None

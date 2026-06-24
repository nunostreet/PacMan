class Ghost:
    """Representa um fantasma no jogo.

    Attributes:
        x: Posição horizontal atual.
        y: Posição vertical atual.
        start_x: Posição horizontal do canto de origem (para respawn).
        start_y: Posição vertical do canto de origem (para respawn).
        edible: True se o fantasma pode ser comido pelo Pacman.
        respawn_timer: Segundos restantes até o fantasma reaparecer (0 = ativo)
    """

    def __init__(self, start_x: int, start_y: int) -> None:
        """Inicializa o fantasma no canto indicado.

        Args:
            start_x: Posição horizontal inicial.
            start_y: Posição vertical inicial.
        """
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.edible: bool = False
        self.respawn_timer: float = 0

    def move(
            self,
            neighbors: dict[tuple[int, int], list[tuple[int, int]]],
            pacman_pos: tuple[int, int]
            ) -> None:
        """Move o fantasma autonomamente com base no modo atual.

        Args:
            neighbors: Lista de adjacência do labirinto.
            pacman_pos: Posição atual do Pacman (x, y).
        """

        if self.respawn_timer > 0:
            return
        best_dist, worst_dist = 1000, 0
        options = neighbors[(self.x, self.y)]
        if not options:
            return
        get_close = options[0]
        move_away = options[0]
        for neighbor in options:
            distance = (
                abs(neighbor[0] - pacman_pos[0])
                + abs(neighbor[1] - pacman_pos[1])
            )
            if distance < best_dist:
                best_dist = distance
                get_close = neighbor
            if distance > worst_dist:
                worst_dist = distance
                move_away = neighbor

        if self.edible:
            self.x, self.y = move_away
        else:
            self.x, self.y = get_close

    def respawn(self, timer: float) -> None:
        """Marca o fantasma como comido e arranca o timer de respawn.

        Args:
            timer: Segundos até o fantasma reaparecer.
        """
        self.respawn_timer = timer
        self.edible = False

    def update(self, dt: float) -> None:
        """Atualiza o timer de respawn e repõe o fantasma quando termina.

        Args:
            dt: Tempo em segundos desde o último frame.
        """
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.x = self.start_x
                self.y = self.start_y

import pygame
from interface.interface_screen import InterfaceScreen


class GameOver(InterfaceScreen):
    """Ecrã mostrado quando o jogador perde.

    Também usado como classe base para ``Victory``, que apenas muda
    o título apresentado.
    """

    def __init__(self, win: pygame.Surface, width: int, height: int):
        """Inicializa o ecrã com a pontuação e nome de jogador por omissão.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        super().__init__(win, width, height)
        self.quit = False
        self.score = 0
        self.player_name = ""
        self.title = "GAME OVER"

    def draw_screen(self, score: int,):
        """Desenha o título, a pontuação final e a entrada de nome atual.

        Args:
            score: A pontuação final do jogador a apresentar.
        """
        content = []
        game = self.font.render(f"{self.title}", True, 'white')
        content.append(game)
        sco = self.font.render(f"Final Score: {score}", True, 'white')
        content.append(sco)
        name = self.font.render(
            f"Player Name: {self.player_name}", True, 'white')
        content.append(name)
        for i in range(len(content)):
            y = (i + 1) * (self.HEIGHT / (len(content) + 1))
            text_rect = content[i].get_rect()
            text_rect.center = (self.WIDTH // 2, y)
            self.WIN.blit(content[i], text_rect)

    def handle_events(self):
        """Processa eventos de input para editar e submeter o nome.

        Trata o fecho da aplicação, o backspace para apagar um
        caracter, a adição de carateres alfanuméricos/espaço (até 10),
        e o Enter para submeter.

        Returns:
            O nome do jogador introduzido se o Enter foi premido, caso
            contrário ``None``.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        return self.player_name
                else:
                    if len(self.player_name) < 10 and (
                        event.unicode.isalnum() or event.unicode == " "
                    ):
                        self.player_name += event.unicode
        return None

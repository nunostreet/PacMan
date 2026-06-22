from mazegenerator import MazeGenerator  # type: ignore[import-untyped]


mg = MazeGenerator(
    size=(15, 15),   # tamanho do labirinto (colunas, linhas)
    perfect=True,    # labirinto "perfeito" (sem ciclos, solução única)
    seed=42          # seed para reproduzir o mesmo labirinto
)
mg.generate()

for row in mg.maze:
    print(row)
print(len(mg.maze))

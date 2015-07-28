# PONG GAME
Um jogo no estilo pong construído com python.

No seu terminal, digite o comando abaixo:
```
$ python pong_game
```
##Controles
  - Jogador 1
    - **W** Mover para cima
    - **S** Mover para baixo
    
  - Jogador 2
   - **O** Mover para cima
   - **L** Mover para baixo
   
##Jogabilidade
O jogo é um simples Pong. Ganha aquele que tem mais pontos, mas a dificuldade aumenta com o tempo a medida que a velocidade da bola também aumenta.
  
##Por dentro
O sistema foi construido em cima da biblioteca tkinter presente no python. Para ver o debug e como os vetores se comportam, habilite o debug na classe Application dentro do Módulo Kernel.
```python
#Kernel.py

class Application(Tk):
    width = 800
    height = 600
    frame_rate = 60  # fps
    canDebug = False # Altere esta variável para True
```

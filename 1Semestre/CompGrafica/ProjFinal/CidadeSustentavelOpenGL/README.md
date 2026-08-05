# Cidade Sustentavel Interativa

Projeto de Computacao Grafica feito com OpenGL.

Objetivo

O programa simula uma pequena cidade em forma de maquete 3D. A proposta e mostrar, de maneira visual e interativa, como algumas acoes sustentaveis podem melhorar o ambiente urbano ao longo do tempo.

## Publico-alvo

O projeto e destinado a estudantes e pessoas interessadas em sustentabilidade, meio ambiente e planejamento urbano basico.

## Como usar

Ao executar o programa, a cidade comeca em um estado poluido. O jogador possui dinheiro limitado e 180 segundos para aumentar o indice ambiental ate pelo menos 85%.

As melhorias sao aplicadas em etapas. Cada acao custa dinheiro, altera a aparencia da cidade e reduz a poluicao. Quanto mais rapido e economico for o processo, maior sera a pontuacao final.

Controles:

- `W`, `A`, `S`, `D`: mover a camera, inclusive em diagonal ao segurar mais de uma tecla
- `Q` e `E`: subir e descer a camera
- Mouse com botao esquerdo pressionado: direcionar a camera
- Setas: girar a camera como alternativa
- `1`: plantar uma arvore, custo R$ 50
- `2`: instalar um painel solar, custo R$ 150
- `3`: construir uma turbina eolica, custo R$ 300
- `4`: ampliar ciclovias e transporte limpo, custo R$ 250
- `5`: aprovar lei antifumaca, custo R$ 400
- `Espaco`: exibir aviso sobre melhorias em etapas
- `R`: reiniciar a cidade
- `Esc`: sair

## Regras do jogo

- Dinheiro inicial: R$ 2600
- Tempo limite: 180 segundos
- Objetivo: atingir 85% de indice ambiental
- Pontuacao final: indice ambiental, dinheiro restante e tempo economizado
- A lei antifumaca reduz a poluicao gradualmente depois de aprovada
- O ceu, a fumaca, as arvores, os paineis solares, as turbinas e os veiculos mudam conforme as acoes do jogador

## Elementos de Computacao Grafica usados

- Objetos 3D modelados com primitivas geometricas
- Transformacoes de translacao, rotacao e escala
- Camera livre com movimentacao pelo teclado
- Iluminacao basica com uma fonte de luz representando o Sol
- Sombra projetada dos objetos no solo a partir da posicao do Sol
- Texturas PNG autorais geradas pelo proprio programa
- Transparencia para representar fumaca
- Animacao de carros, bicicletas e turbinas eolicas
- HUD organizado com dinheiro, tempo, poluicao, progresso e indice ambiental

## Como executar

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python cidade_sustentavel.py
```

Na primeira execucao, o programa cria automaticamente a pasta `textures/` com as texturas PNG usadas na cena.

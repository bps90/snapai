# Reproduzindo os Experimentos do Artigo

Este documento descreve como reproduzir os experimentos do artigo “Um Simulador de Protocolos e Algoritmos de Redes Escrito em Python”.

# Ping Pong

Primeiramente, vamos reproduzir o experimento de ping pong. O experimento
consiste em dois nós que enviam mensagens um para o outro. As mensagens
são enviadas com uma cor aleatória no conteúdo, que é usada pelo nó receptor
para se colorir.

*Se você ainda não fez o tutorial #Getting Started no README, faça isso
    antes de reproduzir o experimento.

1.Navegue até a pasta raiz do SNAPPY no seu terminal.
2.Execute o seguinte comando para iniciar o simulador:
```bash
$ source activate mobenv
```
```bash
$ python manage.py runserver
```
3.Abra seu navegador e acesse [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/).
4.Abra o menu de configurações clicando no botão “Show/Hide configurations” caso ainda não esteja aberto.
5.Selecione o projeto “Sample1” no dropdown de seleção de projeto.
6.Verifique se o restante das configurações está definida conforme abaixo:
    - Nó: sample1:pingpong_node
    - Número de Nós: 2
    - Tamanho dos nós: 10 # você pode alterar esse valor para visualizar melhor os nós
    - Dimensão X: 1000
    - Dimensão Y: 1000
    - Modelo de Distribuição: linear_dist
    - Orientação: horizontal
    - Posição da linha: 0
    - Número de nós (para a seção Parâmetros do Modelo de Distribuição): 2
    - Modelo de Mobilidade: random_walk
    - Intervalo de Velocidade: 0,
    - Intervalo de Direção (radianos): 0,6.
    - Priorizar Velocidade: Não
    - Tempo de Viagem: 70
    - Modelo de Conectividade: qudg_connectivity
    - Raio Máximo: 1000
    - Raio Mínimo: 800
    - Probabilidade de Raio Grande: 0,
    - Modelo de Confiabilidade: reliable_delivery
    - Modelo de Interferência: probability_interference
    - Intensidade: 5
    - Modelo de Transmissão de Mensagem: random_time
    - Tempo Mínimo de Transmissão Aleatória: 2
    - Tempo Máximo de Transmissão Aleatória: 4
7.Clique no botão “Submit” no final do formulário.
8.Clique no botão “Initialize” para redefinir as variáveis da simulação e posicionar os nós no cenário.
9.Defina o número de rodadas para 60.
10.Defina a taxa de atualização para 15.
11.Defina os FPS da simulação para 60.
12.Clique no botão “Run” para iniciar a simulação.
Você deverá ver os nós se movendo no cenário e enviando mensagens um para o
outro. As mensagens são coloridas, e os nós receptores mudam sua cor para a
cor da mensagem recebida. Você pode ver quando uma mensagem é descartada
ou entregue com sucesso no console integrado. Quando os nós perdem a conexão
ou se reconectam, uma mensagem é exibida no console de logs.
13.Para manter os IDs dos nós sempre visíveis, clique e segure no botão
“Show IDs”, mova o mouse para fora do botão e solte o botão do mouse.
14.Para manter as setas sempre visíveis, repita o procedimento do passo 13,
mas com o botão “Show Arrows”.
15.Para parar a simulação, clique no botão “Stop”.
16.Insira os IDs dos nós nos campos “Node 1” e “Node 2” e clique no botão
“Distance” para visualizar a distância euclidiana entre os dois nós.

# Shortest Path + Node2Vec

Agora vamos reproduzir os experimentos do caminho mais curto com Node2Vec.
O experimento de caminho mais curto consiste em encontrar o menor caminho
entre dois nós no cenário. O experimento Node2Vec consiste em executar o
algoritmo Node2Vec no cenário atual.

- Se você ainda não fez o tutorial #Getting Started no README, faça isso antes de reproduzir o experimento.
1.Navegue até a pasta raiz do SNAPPY no seu terminal.
2.Execute o seguinte comando para iniciar o simulador:
```bash
    $ source activate mobenv
```
```bash
$ python manage.py runserver
```
3.Abra seu navegador e acesse [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/).
4.Abra o menu de configurações clicando no botão “Show/Hide configurations” caso ainda não esteja aberto.
5.Selecione o projeto “Sample4” no dropdown de seleção de projeto.
6.Verifique se o restante das configurações estão definidas conforme abaixo:
    - Mensagens NACK Ativadas: Sim
    - Nó: sample5:ping_node
    - Número de Nós: 100
    - Tamanho dos nós: 3
    - Dimensão X: 10000
    - Dimensão Y: 10000
    - Modelo de Distribuição: circular_dist
    - Número de nós (para a seção Parâmetros do Modelo de Distribuição): 100
    - Ponto Médio: 5000,
    - Direção de Rotação: anti-horário
    - Raio: 500
    - Modelo de Mobilidade: random_walk
    - Intervalo de Velocidade: 100,
    - Intervalo de Direção (radianos): 0,6.
    - Priorizar Velocidade: Não
    - Distância de Viagem: 500
    - Modelo de Conectividade: qudg_connectivity
    - Raio Máximo: 500
    - Raio Mínimo: 200
    - Probabilidade de Raio Grande: 0,
    - Modelo de Confiabilidade: reliable_delivery
    - Modelo de Interferência: no_interference
    - Modelo de Transmissão de Mensagem: random_time
    - Tempo Mínimo de Transmissão Aleatória: 1
    - Tempo Máximo de Transmissão Aleatória: 10
7.Clique no botão “Submit” no final do formulário.
8.Clique no botão “Initialize” para redefinir as variáveis da simulação e
posicionar os nós no cenário.
9.Clique no botão “Show/Hide add nodes form” para abrir o formulário.
10.Altere os seguintes parâmetros no formulário:
    - Raio (para a seção Parâmetros do Modelo de Distribuição): 1500
    - Raio Máximo (para a seção Parâmetros do Modelo de Conectividade): 1000
    - Raio Mínimo (para a seção Parâmetros do Modelo de Conectividade): 500
11.Clique no botão "Add to the simulation" para adicionar o novo lote de nós à simulação.
12.Volte ao formulário de Adicionar Nós e altere os seguintes parâmetros:
    - Raio (para a seção Parâmetros do Modelo de Distribuição): 2500
    - Raio Máximo (para a seção Parâmetros do Modelo de Conectividade): 1200
13.Clique no botão "Add to the simulation" para adicionar o novo lote de
nós à simulação.
14.Defina o número de rodadas para 1.
15.Clique no botão “Run” para iniciar a simulação.
16.Insira os IDs dos nós nos campos “Node 1” e “Node 2” e clique no botão “Shortest Path” para executar o algoritmo de caminho mais curto
(no artigo, testamos com os nós 150 e 300).
Você deverá ver o menor caminho entre os dois nós no grafo com setas vermelhas.
17.Insira o número de dimensões no campo “Dimensions” e clique no botão “Run Node2Vec Algorithm” para rodar o algoritmo Node2Vec (no artigo, testamos com 4 dimensões).
Você deverá ver o resultado do algoritmo Node2Vec no gráfico.



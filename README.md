# netflix challenge
## Sistema de recomendação de filmes baseado em similaridade de usuários


### Introdução  
O desafio netflix consistia na criação de um sistema de recomendação de filmes para os usários. A informação disponivel para realizar essa análise eram uma lista de filmes e uma lista de avaliações de usuários. A partir dessas informações, o sistema deveria recomendar filmes para os usuários que ainda não avaliaram.  
Desse modo, o problema se resumia a "predizer" a nota que um dado usuário daria para um filme que ele ainda não assistiu (e por consequência, não avaliou).
O vencedor do desafio utilizaou um algoritmo de decomposição SVD (Singular Value Decomposition) para realizar essa predição. Uma versão dessa ideia é implementada nesse projeto.

### Qual a idéia por trás do algoritmo?
O pressuposto por trás da idéia implementada é a de que, cada usuário, pode ser entendentido como uma combinação de perfis "gerais". Por exemplo, um usuário pode ser entendido como uma combinação de perfis de "usuários que gostam de filmes de ação", "usuários que gostam de filmes de comédia" e "usuários que gostam de filmes de terror", com pesos diferentes. Então uma pessoa que gosta bastante de filme de comédia e ação, porém odeia filmes de terror, teria um valor alto multiplicando o "vetor_perfil comédia" e alto para "vetor_perfil ação", mas baixo para "vetor_perfil terror".


### O que é SVD?  
SVD é uma técnica de decomposição de matrizes em matrizes que representam os autovalores e autovetores da matriz original. Para realizar o SVD deve-se determinar os autovalores e autovetores da matriz $AA^T$. 
A decomposição SVD é dada por:  

$$ A = U \Sigma V^T $$  

Em que $U$ é uma matriz com os autovetores da matriz $AA^T$, $V$ é uma matriz com os autovetores da matriz $A^TA$ e $\Sigma$ é uma matriz diagonal com a raiz dos autovalores de $AA^T$. Ou seja, temos a matriz com a raiz dos autovalores e duas matrizes com autovetores, uma dos vetores coluna de $A$ e outra dos vetores linha.

### Qual a vantagem de usar SVD?
A vantagem de usar SVD é que, ao decompor a matriz $AA^T$ em matrizes com autovetores e autovalores, é possível retirar a influência de "perfis" menos expressivos, que, em vias gerais, podem ser consideradas ruído. Isso é feito selecionando apenas os $k$ maiores autovalores e seus respectivos autovetores. Com isso somente os k perfis mais expressivos serão considerados e eles determinarão as notas que o usuário daria para os filmes que ele ainda não avaliou.

### Como funciona o algoritmo?
O algoritmo de teste funciona da seguinte forma:
1. Carrega os dados de filmes e avaliações
2. Cria uma matriz de avaliações de usuários por filmes
3. Substitui a nota de um usuário por uma nota aleatória
4. Calcula a decomposição SVD da matriz de avaliações
5. Retira os últimos $k$ autovalores e seus respectivos autovetores (o valor de k é definido a partir de um estudo do gráfico dos autovalores)
6. Reconstrói a matriz de avaliações com os autovalores e autovetores selecionados
7. Realiza a comparação da nota original com a nota predita

O algoritmo real é semelhante, com a diferença de que ele não realiza a substituição da nota por uma nota aleatória, mas sim, realiza a predição de notas para espaços vazios no dataframe (valores NAN após o pivot_table), utilizando um valor padrão ou aleatório para representar essa nota a ser predita.

### O que foi implementado?
Foi implementado o algoritmo citado e realizado 1724 experimentos, escolhendo um valor aleátorio a cada iteração, realizada a inserção de ruído, calculado o svd, a retirada de k valores e a reconstrução. O valor absoluto da diferença entre o esperado e o predito estão no "diferenças.txt".
O arquivo de escrita é o escrever_txt.py.  
Porém, para chegar nesse código foram realizadas análises explorátorias no main.ipynb, nele estão presentes as etapas realizadas que serão apresentadas abaixo:
1. Criação do dataframe a partir da leitura dos dados.
2. Criação da tabela com usuário nas linhas, filmes na coluna e nota nas células.
3. Realiza a cópia da matriz e escolhe um valor (que não seja NaN) e substitui por um valor aleátorio entre 0,5 e 5,0.
4. Preenche as celulas com NaN com 2,75 (o meio do intervalo de notas possíveis).
5. Para a escolha do $K$, foi realizado um estudo dos autovalores. O gráfico dos autovalores é apresentado abaixo:  

![sigma_svd](SigmaSVDOutlier.png)  

Porém, com o primeiro autovalor sendo um Outilier, o removemos e o gráfico ficou assim:

![sigma_svd_sem_outlier](SigmaSVD.png)  
Dessa forma, atribuimos o valor 20 para $K$, pois é o valor que, por meio de varios testes, apresentou o melhor resultado e ser onde o gráfico começa a se estabilizar.

6. Em seguida é realizado o procedimento explicado na seção anterior.

O histograma construido é apresentado abaixo:
![histograma_um_valor](hist_distribuicao_com_um_so_valor_alterado.png)


### Teste de estresse
No código foi realizado um teste de estresse. Ele consiste em averiguar a eficácia do algoritmo com o aumento de valores "sujos" (aleatórios) na matriz. Para isso, foi realizado um loop que aumenta o número de valores aleatórios na matriz, até chegar a uma certa quantidade $n$ de valores ruidosos. Em seguida, ele realiza o procedimento descrito na seção anterior. Isso foi realizado 700 vezes para cada $n$. O resultado é apresentado abaixo (o gráfico é salvo no arquivo "distribuicao_teste_de_estresse.png")

![histograma_teste_estresse](distribuicao_teste_de_estresse.png)

Como pode ser observado, são realizados 4 ensaios, com $n$ igual a 100, 200, 500 e 1000. Além disso, foram selecionados 700 valores do caso com somente um valor ruidoso, para realizar uma comparação. A partir da análise, é possível perceber que, mesmo com um aumento, a eficácia do algoritmo se mantêm próxima do caso base (apenas um valor ruidoso). 

### Resultados e Discussão
A partir da análise dos dados levantados, pode-se perceber que o algoritmo é razoalvemente eficaz para realizar a recomendação de filmes para multiplos usuários, sem grande perda na eficácia. Essa característica é relavante para sistemas em produção, tendo em vista a grande demanda para realizar recomendação de filmes para multiplos usuários.  
Dito isso, cabem algumas ressalvas. O algoritmo claramente subestima a nota que o usuário daria, então ocorreria uma série de casos em que o algoritmo considera que o usuário não gostaria de um filme, quando na verdade ele deveria ser recomendado. Esse ponto é relevante para um algoritmo de recomendação. Então alterações no algoritmo para gerar uma distribuição com maior concentração na esquerda devem ser consideradas, para permitir um desempenho de fato positivo para um sistema em produção.


### Como instalar?  
Para garantir o funcionamento da aplicação é recomedado a criação de um ambiente virtual (venv) para instalar as dependência, como apresentado em https://docs.python.org/3/library/venv.html.  
Em seguida, deve-se ativar o ambiente virtual e instalar as dependências através do comando:  
```pip install -r requirements.txt```

Para visualizar os graficos, rode o arquivo demo.py na sua IDE, ou através do comando (no diretório raiz do repositorio):  
```python demo.py```	

Na main.ipynb é possivel ver a construção do algoritmo e a análise dos dados.


Protinho agora é só rodar o arquivo em sua IDE ou Jupyter notebook.
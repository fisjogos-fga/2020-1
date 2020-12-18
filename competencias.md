Python
-======

## py-flow: Utilizar as estruturas de controle if/elif/else, for e while
* Condicionais com várias alternativas.
* Uso da função range() no for.
* Saber identificar oportunidades para usar o for ou o while.

## py-seq0: Conhecer e utilizar a sintaxe de operações básicas com listas e dicionários
* Índices e fatiamento.
* Descobrir tamanho.
* Iteração em um laço for.

## py-seq1: Usar funçoes de listas e dicionários em problemas de programação
* Uso de for + list.append para construir uma lista.
* Uso de for + `D[k] = v` para construir um dicionário.

## py-str0: Usar métodos e funções para identificar propriedades de strings
* Identificar propriedades básicas de strings (ex.: isupper/islower/startswith.
* Indexação e fatiamento para selecionar sub-strings ou caracteres.

## py-str1: Usar métodos para fatiar e construir strings
* Separar partes de uma string (fatiamento e métodos como split ou partition).
* Juntar strings (join ou soma de strings).
* Usar f-strings ou o operador de formatação para interpolar strings.

## py-rec: Utilizar recursão para resolver problemas de programação
* Identificar situações arquetípicas onde é possível trocar um laço por recursão.
* Identificar problemas onde é simples transformar uma solução recursiva em procedural ou vice-versa.
* Aplicar recursão para resolver algum problema de programação.

## py-hifn: Aplicar funções de segunda ordem como map, filter, sort, etc em problemas de programação
* Reconhecer que é possível passar funções como argumentos.
* Identificar algumas funções que podem (opcionalmente ou obrigatoriamente) receber outras funções.
* Criar pequenas funções para passar para funções de segunda ordem.

## py-pep8: Conhecer boas práticas de estilo de programação
* Uso de comentários e nomes informativos.
* Organização do código em funções.
* Familiaridade com pelo menos uma ferramenta como Black, pep8, pylint ou flake8.

## py-bug*: Encontrar e reportar bug não trivial em projeto relacionado ao conteúdo da disciplina
* Bug pode ser identificado no pyxel, pymunk ou em algum outro projeto relacionado à disciplina.
* É necessário comunicar o bug utilizando o sistema de issues do Github e fornecer as informações necessárias para reprodução do mesmo que forem requisitadas pelo desenvolvedor.
* Pedido de novas funcionalidades não serão considerados.
* Bugs triviais como erros de escrita ou pequenas falhas na documentação só serão considerados se tiverem um patch aprovado no projeto principal.

## py-pr*: Realizar um pull request para projeto utilizado na disciplina ou relacionado ao conteúdo de compiladores
* PR pode ser aceito em um projeto de terceiros ou no projeto do motor de jogos
* criado na disciplina.

## py-package*: Empacotar o projeto de programação desenvolvido na disciplina usando boas práticas de empacotamento e distribuição da comunidade
* Publicar o projeto no PyPI (ou equivalente, se for em outra linguagem).
* Criar repositório público com boas práticas de publicidade.

## py-ci*: Instrumentar um projeto de programação desenvolvido na disciplina com testes e integração contínua
* Instrumentar repositório com testes unitários com boa cobertura.
* Configurar a integração contínua para operar em cada commit do Github.


Motor de física
===============

## ge-body1: Implementar uma classe que representa partículas
* Implementar propriedades de posição, velocidade e massa.
* Implementar um integrador simples.
* Implementar cálculo de grandezas físicas elementares.

## ge-body2: Implementar uma classe que representa corpos rígidos
* Incorporar grandezas angulares à classe Body.
* Integrar equações angulares.
* Incorporar ponto de aplicação da força aos cálculos de resposta angular.

## ge-body3: Implementar uma classe que representa alguma figura geométrica
* Realizar cálculos de inércia e massa para figuras geométricas específicas.
* Testes de colisão entre figuras de mesmo tipo.

## ge-space1: Implementar classe mundo/Space responsável por gerenciar objetos físicos
* Realizar registro de objetos no mundo.
* Atualização de velocidades e posições de todos objetos gerenciados.  

## ge-space2: Implementar colisões na classe "Space"
* Implementar broad-phase e narrow phase.
* Incorporar colisões no loop de atualização da física.

## ge-poly*: Implementar uma classe que representa polígonos convexos
* Realizar cálculos de inércia, massa e testes de validação.
* Testes de colisão.

## ge-eventos1*: Implementar suporte a eventos de colisão
* Identificação de fases/eventos numa colisão.
* Registro de callbacks de colisão.

## ge-eventos2*: Implementar suporte a eventos programados
* Registro de callbacks de eventos programados.
* Eventos programados para operar a cada frame.
* Animações.


Leis de Newton
==============

## phys-vec: Utilizar a segunda lei de Newton em sua forma vetorial
* Enununciar e formular leis de Newton na forma vetorial.

## phys-quad: Integrar equações de sistemas físicos usando método de Euler
* Integrar equações de movimento utilizando o método de Euler.
* Incluir método de integração em jogo ou simulação interativa.
  
## phys-energia: Compreender e utilizar o conceito de energia
* Identificar situações onde existe conservação de energia.
* Utilizar conservação de energia como forma de validação de uma simulação.
* Calcular energia potencial e cinética de sistemas simples.

## phys-momento: Compreender o conceito de momento linear e conservação do momento total
* Calcular e ser capaz de implementar cálculo de momento linear em código. 
* Utilizar o momento para validar sistemas físicos fechados.
* Reconhecer o papel do momento linear na resolução de colisões.

## phys-impulso: Formular e compreender o conceito de impulso
* Calcular o impulso de forças.
* Papel do impulso na resolução de forças instantâneas e colisões.

## phys-pot: Calcular forças a partir da energia potencial
* Calcular forças a partir da energia potencial.
* Utilizar cálculo da energia total como método de validação.

## phys-atrito: Modelo de Coulomb de atrito
* Compreender grandezas principais do atrito no modelo de Coulomb.
* Identificar a força normal e sua origem.
* Apreciar efeito do coeficiente de atrito.

## phys-viscoso: Modelo de dissipação linear
* Compreender conceitos básicos de modelo de dissipação linear.
* Uso da força dissipativa como estratégia para estabilizar uma simulação. 

## phys-gravidade: Modelo de aceleração uniforme
* Compreender e implementar um modelo de aceleração uniforme (como a gravidade local)
* Compreender as dimensões e ser capaz de dimensionar valores de aceleração e outras grandezas em modelos de aceleração uniforme.

## phys-pot2*: Criar modelos de força a partir da energia potencial
* Modificar modelos de força a partir da energia potencial.
* Modificar a energia potencial para aumentar a estabilidade do sistema.
* Utilizar cálculo da energia total como método de validação.

## phys-simpletic*: Utilizar e implementar métodos simpléticos para implementar as equações de movimento
* Compreender a necessidade de utilizar métodos simpléticos em jogos.
* Identificar versões simpléticas e não-simpléticas do método de Euler.
* Implementar método de segunda ordem como Leapfrog.

## phys-hiord*: Utilizar métodos de alta ordem para a integração das leis de movimento
* Implementar método como Runge-Kutta para resolução de EDOs.
* Identificar situações na mecânica do jogo onde o método pode ser relevante.

## phys-part*: Implementar sistemas de partículas para produzir efeitos de partículas
* Implementar algum efeito de partículas com sistemas sem colisões.
* Sistema deve possuir representação visual e física implementada em código.


Corpos Rígidos
==============

## mi-def: Compreender intuitivamente e conhecer as equações que definem o momento de inércia de um corpo
* Compreender a relação entre momento de inércia e energia cinética rotacional.
* Compreender a relação entre momento de inércia e torque.
* Compreender que o momento de inércia é uma grandeza relativa ao eixo de rotação.

## mi-calc: Calcular momento de inércia de um sistema de partículas
* Calcular o momento de inércia de um sistema discreto de partículas a partir da definição.

## mi-eixo: Utilizar o teorema dos eixos paralelos para simplificar o cálculo do momento de inércia de objetos
* Enunciar corretamente a fórmula para o teorema dos eixos paralelos.
* Realizar corretamente a transposição do momento de inércia entre dois eixos paralelos.
* Entender a importância do centro de massa no cálculo e utilização do teorema.

## mi-objs*: Calcular momento de inércia de figuras geométricas simples utilizando integrais
* Utilizar integrais para calcular o momento de inércia de figuras simples.
* Realizar cálculo unidimensional ou utilizando elementos de integração baseados em figuras com o momento de inércia conhecido. 


Colisões
========

## col-circ: Identificar presença de colisões em círculos
* Detecção de colisão entre círculo-círculo.
* Identificação da força normal.
* Identificação do ponto de contato.

## col-aabb: Identificar presença de colisões em AABBs
* Detecção de colisão entre AABB-AABB.
* Identificação da força normal.
* Identificação do ponto de contato.

## col-params: Identificar parâmetros físicos de uma colisão
* Ponto de contato.
* Direção normal à colisão.
* Coeficiente de atrito e restituição.
* Representação em código.

## col-solve: Resolver colisões simples
* Identificação de forças e impulsos.
* Solução de colisões binárias.
* Implementação em código.

## col-poly*: Identificar presença de colisões em polígonos
* Detecção de colisão entre polígono-polígono.
* Identificação da força normal.
* Identificação do ponto de contato.

## col-solve2*: Resolver colisões com atrito
* Inclusão de atrito na colisão binária.

## col-solve3*: Resolver colisões compostas
* Sistemas iterativos de solução.
* Permanência de parâmetros de colisão.


Vínculos
========

## vi-mola: Compreender modelo de oscilador harmônico
* Compreensão das grandezas que descrevem uma mola idealizada.
* Entendimento intuitivo dos coeficientes de mola e dissipativo.

## vi-pivos: Modelo de pivoteamento e distâncias fixas
* Apreciar fundamentos e conceitos básicos da formulação matemática de problemas de vínculo.
* Compreender qualitativamente os problemas numéricos associados à manutenção de condições de vínculo.
* Entender forças e vínculos necessários para manter as condições de vínculo.

## vi-vinculos: Implantar sistemas com vínculos na Pymunk
* Ser capaz de manipular em código e dominar os conceitos básicos a respeito de vínculos utilizando a Pymunk.

## vi-contato*: Colisões como problemas de vínculo
* Compreender colisões como problemas de vínculos.
* Compreender os desafios matemáticos na resolução de sistemas de inequações vindas de problemas de colisão.
   
## vi-vinculo*: Implementar problema de vínculo manualmente
* Implementar algum sistema de vínculo manualmente no motor de jogos da turma.
* Implementar uma estratégia de estabilização.


Álgebra linear
==============

## al-vec: Implementar vetores em código
* Implementar uma classe que representa vetores 2D em código.
* Operações aritméticas.
* Cálculo de características importantes como tamanho, ângulo e outros.

## al-soma-vec: Realizar e interpretar a soma vetorial
* Compreender o significado geométrico de uma soma vetorial pela regra do paralelogramo.
* Operacionalizar a soma vetorial e traduzir em código.

## al-prod: Realizar e interpretar o produto escalar
* Utilizar o produto escalar para calcular projeções e cálculo do ângulo entre vetores.
* Operacionalizar o produto escalar e traduzir em código.

## al-linhas: Representação de retas
* Representação algébrica da equação da reta.
* Parametrização vetorial.
* Problemas de interseção e entre retas e projeções de segmentos.

## al-vec-prod: Realizar e interpretar o produto vetorial
* Interpretar o produto vetorial em termo das projeções ortogonais.
* Compreender o papel da dimensionalidade no produto vetorial.
* Operacionalizar o produto vetorial e traduzir em código.

## al-mat: Realizar operações básicas com matrizes
* Soma/subtração e multiplicação matricial.
* Realizar multiplicação entre matrizes e vetores.
* Reconhecer papel da dimensionalidade no produto matricial.

## al-transf: Compreensão geométrica de transformações lineares
* Criar matrizes de mudança de escala e cisalhamento.
* Criar e manipular matrizes de rotação 2D.
* Transformações de espelhamento

## al-afins: Compreender e formular transformações afins 2D
* Representação puramente matricial e matriz/vetor de transformação afim.
* Compreensão intuitiva de transformações afins.
* Formulação de movimentos de câmera e movimento relativo de objetos como transformações afins.

## al-mat*: Implementar matrizes em código
* Implementar uma classe que representa matrizes 2x2 em código.
* Operações aritméticas.
* Interação com vetores.

## al-vec3*: Implementar vetores 3D em código
* Implementar uma classe que representa vetores 3D código.
* Operações aritméticas.
* Interação com vetores.

## al-xy*: Realizar contribuções para biblioteca XY
* Submeter um PR para a https://github.com/fabiommendes/xy/ ou alguma outra biblioteca de álgebra linear em baixa dimensionalidade.


Projeto de jogos
================

## jogo-classico: Consegue implementar um jogo clássico com física simples
* Implementou jogo com física simples como pong, flappy bird ou outros.
* Interações implementadas sem ajuda de um motor de física.

## jogo-phys: Implementar jogo com mecânica baseada em física
* Concebeu e implementou jogo com mecânica que utiliza física.
* Conseguiu formular interações em termo de forças ou impulsos.

## jogo-pymunk: Incorporou motor de física ao jogo
* Concebeu e implementou jogo com mecânica que utiliza física.
* Incorporou motor de física como pymunk ou box2D ao jogo.

## jogo-input: Implementou interação com o usuário
* Jogo utiliza mecanismos de entrada de dados pelo usuário (mouse ou teclado).

## jogo-menu*: Jogo possui menus de incialização
* Jogo possui menus e telas intermediárias de configuração/inicialização.

## jogo-fase*: Jogo possui mais de uma fase
* Jogo possui 2 ou mais "fases" e consegue trocar os objetos de Space durante a utilização.

## jogo-criativo*: Projeto faz uso criativo da física na mecânica de jogo
* Projeto faz uso criativo da física para estabelecer a mecânica de jogo.

## jogo-polido*: Interação com usuário na mecânica principal não apresenta defeitos  
* Jogo possui interações equilibradas e bem calibradas.
* Jogo implementa detalhes não-triviais na física para melhorar a interação com o usuário.
* Jogo conseguiu eliminar quase todos bugs óbvios na interação com o usuário.  

## jogo-divertido*: Jogo baseado em física com alta jogabilidade
* Jogo possui alta jogabilidade e produz engajamento.

## jogo-arte*: Jogo apresenta arte original de boa qualidade
* Produziu arte original e de boa qualidade.
* Arte pode incluir imagens, sons ou músicas.


Genérico
========

## conteudo-arte*: Produziu material com alta qualidade estética/artística
* Criou material de estudo, ou material para o projeto final com expressão de qualidade artística.

## conteudo-texto*: Produziu material com qualidade literária
* Criou material de estudo, ou material para o projeto final com ótima qualidade de texto. 

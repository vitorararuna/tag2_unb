# tag2_unb

* Projeto 2 da disciplina de Teoria e Aplicação de Grafos - Universidade de Brasília

* ALGORITMO ADAPTADO:
  * O algoritmo foi desenvolvido com base nos documentos abaixo, onde o emparelhamento de casais é realizado com a finalizade de formaçõ de casais   
      *  https://medium.com/@satyalumesh/gale-shapley-algorithm-for-stable-matching-easyexpalined-17ee51ec0dfa
      *  https://www.puc-rio.br/ensinopesq/ccpg/pibic/relatorio_resumo2014/relatorios_pdf/ctc/MAT/MAT-Jos%C3%A9%20Eliton%20Albuquerque%20Filho.pdf
  *  A adaptação sugere que sejam criadas 2 listas: uma para as preferências em relação aos estudantes e outra com as preferências em relação aos projetos que estão sendo realizados.
  *  O arquivo de entrada "entradaProj2TAG.txt" é responsável por definir tais relações de preferências.
  *  Em relação às preferências dos projetos, caso o aluno não tenha interesse por um projeto, ele é descartado da lista do mesmo (critério eliminatório). A nota do aluno e sua preferência são critérios usados em ordenamento.
  
* COMO EXECUTAR O ALGORITMO:
  * Basta rodar o comando "python tag.py"

* O QUE O ALGORITMO RETORNA:
  * 10 Primeiras iterações em ordem de projetos
  * Resultado do emparelhamento estável máximo obtido
  * Detalhes dos projetos com vagas preenchidas
  * Detalhes dos projetos com vagas sobrando

## Desafio de Modelagem Dimensional

### Descrição:

##### Objetivo:
Criar o diagrama dimensional – star schema – com base no diagrama relacional disponibilizado.
##### Foco:

Professor – objeto de análise.
Montar o esquema em estrela com o foco na análise dos dados dos professores. Sendo assim, a tabela fato deve refletir diversos dados sobre professor, cursos ministrados, departamento ao qual faz parte, etc.
Obs.: Não é necessário refletir dados sobre os alunos!

O que deve ser feito?
- Deverá ser criada a tabela Fato que contêm o contexto analisado. Da mesma forma, é necessária a criação das tabelas dimensão que serão compostas pelos detalhes relacionados ao contexto.
- Por fim, mas não menos importante, adicione uma tabela dimensão de datas. Para compensar a falta de dados de datas do modelo relacional, suponha que você tem acesso aos dados e crie os campos necessários para modelagem.

Ex: data de oferta das disciplinas, data de oferta dos cursos, entre outros. O formato, ou melhor, a granularidade, não está fixada. Podem ser utilizados diferentes formatos que correspondem a diferentes níveis de granularidade.

## Imagem de referência
<img align="center" src="https://github.com/Judenilson/dio-python-bootcamp/blob/main/power-bi-challenges/power_bi_analyst_star_schema_ref_image.png" />    

## Imagem da Modelagem Dimensional Star Schema
<img align="center" src="https://github.com/Judenilson/dio-python-bootcamp/blob/main/power-bi-challenges/power_bi_analyst_star_schema.png" />    

## Código usado no dbdiagram.io para gerar a modelagem
### https://dbml.dbdiagram.io/docs

enum atuacao {
  "exatas"
  "humanas"
  "saude"
}

Table f_professor {
  id_f_professor integer [pk]
  id_d_data integer 
  id_d_curso integer
  id_d_disciplina integer
  ID_d_departamento integer
  professor_nome varchar[45]
  professor_sobrenome varchar[45]
  professor_area_atuacao atuacao
  professor_carga_horaria time 
}

Table d_data {
  id_d_data integer [pk]
  Data_data datetime
}

enum modalidade {
  "presencial"
  "ead"
}

Table d_curso {
  id_d_curso integer [pk]
  curso_nome varchar[45]
  curso_modalidade modalidade
  curso_duracao time
}

Table d_disciplina {
  id_d_disciplina integer [pk]
  disciplina_nome varchar
  disciplina_carga_horaria time
}

Table d_departamento {
  ID_d_departamento integer [pk]
  departamento_nome varchar[45]
  departamento_campus varchar[45]
}

Ref: d_data.id_d_data > f_professor.id_d_data
Ref: d_curso.id_d_curso > f_professor.id_d_curso
Ref: d_disciplina.id_d_disciplina > f_professor.id_d_disciplina
Ref: d_departamento.ID_d_departamento > f_professor.ID_d_departamento

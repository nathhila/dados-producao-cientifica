-- É NECESSÁRIO PARA O PATH DO CONTAINER NO CASO DE RODAR EM DOCKER, SE RODAR DA FORMA USUAL USAR O PATH ABSOLUTO

\copy producoes_topicos (doi, topico, id_scopus) FROM '../data/producoes_topics.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'UTF8');
\copy producoes (autor, titulo, id_scopus, doi, openalex_titulo, openalex_resumo, ano_publicacao) FROM '../data/producoes.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'UTF8');


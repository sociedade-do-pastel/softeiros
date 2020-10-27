CREATE TABLE public.computador(
       id_computador INT GENERATED ALWAYS AS IDENTITY,
       nome_sala VARCHAR(4) REFERENCES sala(nome_sala)
 );




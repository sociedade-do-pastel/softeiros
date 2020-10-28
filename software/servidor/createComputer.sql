CREATE TABLE IF NOT EXISTS public.computador(
       id_computador INT GENERATED ALWAYS AS IDENTITY,
       nome_sala VARCHAR(4) REFERENCES sala(nome_sala),
       pos_x INT,
       pos_y INT,
       primary key (id_computador)
 );




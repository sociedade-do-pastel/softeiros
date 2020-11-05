CREATE TABLE IF NOT EXISTS public.computador(
       id_computador INT GENERATED ALWAYS AS IDENTITY,
       nome_sala VARCHAR(4) REFERENCES sala(nome_sala) ON DELETE CASCADE,
       pos_x INT NOT NULL,
       pos_y INT NOT NULL,
       em_uso BOOL DEFAULT false,
       primary key (id_computador)
 );






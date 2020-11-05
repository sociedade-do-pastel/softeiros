CREATE TABLE IF NOT EXISTS public.sala(
       nome_sala CHAR(4) NOT NULL UNIQUE,
       hora_fechamento time NOT NULL,
       ip_sala inet NOT NULL,
       primary key (nome_sala)
);



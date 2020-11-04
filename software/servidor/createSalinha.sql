CREATE TABLE IF NOT EXISTS public.sala(
       nome_sala CHAR(4),
       hora_fechamento time,
       ip_sala inet,
       primary key (nome_sala)
);



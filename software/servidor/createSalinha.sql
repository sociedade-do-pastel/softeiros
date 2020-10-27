CREATE TABLE public.sala(
       nome_sala VARCHAR(4),
       hora_fechamento TIMESTAMP,
       ip_sala VARCHAR(12),
       qtd_lugares_disp INT,
       qtd_maxima_lugares INT,

       primary key (nome_sala)
);



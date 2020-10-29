CREATE TABLE IF NOT EXISTS public.sala(
       nome_sala CHAR(4),
       hora_fechamento time,
       ip_sala inet,
       qtd_lugares_disp INT,
       
       primary key (nome_sala)
);



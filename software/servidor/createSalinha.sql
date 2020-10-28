CREATE TABLE IF NOT EXISTS public.sala(
       nome_sala VARCHAR(4),
       hora_fechamento time,
       ip_sala VARCHAR(12),
       qtd_lugares_disp INT,
       
       primary key (nome_sala)
);



CREATE TABLE IF NOT EXISTS public.softwares_disp
(
	nome_software VARCHAR(40),
	id_computador INT REFERENCES computador(id_computador),
	primary key(nome_software, id_computador)
);


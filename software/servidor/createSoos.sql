CREATE TABLE IF NOT EXISTS public.softwares_disp
(
	nome_software VARCHAR(40) NOT NULL,
	id_computador INT REFERENCES computador(id_computador) ON DELETE CASCADE,
	primary key(nome_software, id_computador)
);


CREATE EXTENSION IF NOT EXISTS pgcrypto ;

CREATE TABLE IF NOT EXISTS public.usuario(
       nome_usuario VARCHAR(20) NOT NULL UNIQUE,
       id_user      INT GENERATED ALWAYS AS IDENTITY,
       senha_usuario VARCHAR(100) NOT NULL,
       
       primary key (id_user)              		 
);



CREATE TABLE public.usuario(
       nome_usuario VARCHAR(20),
       id_user      INT GENERATED ALWAYS AS IDENTITY,
       senha_usuario VARCHAR(100),

       primary key (id_user)              		 
);



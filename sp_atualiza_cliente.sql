CREATE PROCEDURE `sp_atualiza_cliente`(
IN PIN_iddadosCli int,
IN PIN_rNomeCli varchar(45),
IN PIN_rEmail varchar(45),
IN PIN_nIdade int,
IN PIN_rLogradouro varchar(85),
IN PIN_nCep varchar(12),
IN PIN_Bairro varchar (45))
BEGIN
	UPDATE primeiroprojeto.tdadoscli set rNomeCli = PIN_rNomeCli, rEmail = PIN_rEmail, nIdade = PIN_nIdade, rLogradouro = PIN_rLogradouro, nCep = PIN_nCep, rBairro = PIN_Bairro
    WHERE iddadosCli = PIN_iddadosCli;
END
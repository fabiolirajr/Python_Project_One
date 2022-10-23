CREATE PROCEDURE `sp_consulta_cliente`(
IN PIN_identificadorcliente int,
OUT POUT_iddadosCli int,
OUT POUT_rNomeCli varchar(45),
OUT POUT_rEmail varchar(45),
OUT POUT_nIdade int,
OUT PIN_rLogradouro varchar(85),
OUT PIN_nCep varchar(12),
OUT PIN_Bairro varchar (45))
BEGIN
	SELECT iddadosCli, rNomeCli, rEmail, nIdade, rLogradouro, nCep, rBairro  INTO POUT_iddadosCli, POUT_rNomeCli, POUT_rEmail, POUT_nIdade, PIN_rLogradouro, PIN_nCep, PIN_Bairro
	FROM primeiroprojeto.tdadoscli 
    WHERE iddadosCli = PIN_identificadorcliente;
END
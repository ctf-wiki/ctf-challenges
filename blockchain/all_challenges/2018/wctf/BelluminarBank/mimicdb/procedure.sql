USE MASTER
GO

DROP PROCEDURE sp_logEvent;
GO

CREATE PROCEDURE sp_logEvent(@Txt varchar(max), @Name varchar(40), @Type varchar(40)) WITH EXECUTE AS OWNER
AS
BEGIN
	DECLARE @query varchar(max);
	SET @Txt = REPLACE(@Txt, "'", "''")
	SET @Name = REPLACE(@Name, "'", "''")
	SET @Type = REPLACE(@Type, "'", "''")
	SET @query = 'EXEC master..spWriteStringToFile ''' + @Txt + ''', ''C:\Users\belluminar\Desktop\webapp\logs\' + @Name + ''', ''' + @Type + '.log''';
	EXECUTE(@query);
END
GO

GRANT EXECUTE ON sp_logEvent to PUBLIC
GRANT VIEW DEFINITION ON sp_logEvent TO PUBLIC

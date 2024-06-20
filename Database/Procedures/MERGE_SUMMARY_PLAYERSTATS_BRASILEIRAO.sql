CREATE OR REPLACE EDITIONABLE PROCEDURE "FOOTSTATS"."MERGE_SUMMARY_PLAYERSTATS_BRASILEIRAO" AS
BEGIN

	DECLARE
		table_exists_1 NUMBER;
	BEGIN
		SELECT COUNT(*)
		INTO table_exists_1
		FROM user_tables
		WHERE table_name = 'TEMP_CONCAT_STRINGS';

		IF table_exists_1 = 1 THEN
			EXECUTE IMMEDIATE 'TRUNCATE TABLE temp_concat_strings';
			EXECUTE IMMEDIATE 'DROP TABLE temp_concat_strings';
		END IF;
	END;

	EXECUTE IMMEDIATE 
	'
	CREATE GLOBAL TEMPORARY TABLE temp_concat_strings
	ON COMMIT PRESERVE ROWS
	AS
	SELECT
		"Hash_ID",
		"Created_Date",
		"Player" || 
		"Nation" || 
		"Position" || 
		"Squad" || 
		"Age" || 
		"Birth_Year" || 
		"Matches_Played" || 
		"Starts" || 
		"Minutes_Played" || 
		"Minutes_90s" || 
		"Goals" || 
		"Assists" || 
		"Goals_Plus_Assists" || 
		"Goals_Excluding_PK" || 
		"Penalty_Kicks" || 
		"Penalty_Kicks_Attempted" || 
		"Yellow_Cards" || 
		"Red_Cards" || 
		"Expected_Goals" || 
		"NonPenalty_Expected_Goals" || 
		"Expected_Assists" || 
		"NonPenalty_Expected_Goals_Plus_Assists" || 
		"Progressive_Carries" || 
		"Progressive_Passes" || 
		"Progressive_Receptions" || 
		"Goals_Per_90_Minutes" || 
		"Assists_Per_90_Minutes" || 
		"Goals_Plus_Assists_Per_90_Minutes" || 
		"Goals_Excluding_PK_Per_90_Minutes" || 
		"Goals_Plus_Assists_Excluding_PK" || 
		"Expected_Goals_Per_90_Minutes" || 
		"Expected_Assists_Per_90_Minutes" || 
		"Expected_Goals_Plus_Assists_Per_90_Minutes" || 
		"NonPenalty_Expected_Goals_Per_90_Minutes" || 
		"NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes" AS CONCAT_STRING,
		ROW_NUMBER() OVER (PARTITION BY "Player", "Squad", "Birth_Year" ORDER BY "Created_Date" DESC) AS RN
	FROM FOOTSTATS.FOOTSTATS_HISTORY_PLAYERSTATS_BRASILEIRAO';

	DECLARE
		table_exists_2 NUMBER;
	BEGIN
		SELECT COUNT(*)
		INTO table_exists_2
		FROM user_tables
		WHERE table_name = 'TEMP_HASH';

		IF table_exists_2 = 1 THEN
			EXECUTE IMMEDIATE 'TRUNCATE TABLE temp_hash';
			EXECUTE IMMEDIATE 'DROP TABLE temp_hash';
		END IF;
	END;

	EXECUTE IMMEDIATE
	'
	CREATE GLOBAL TEMPORARY TABLE temp_hash
	ON COMMIT PRESERVE ROWS
	AS
	SELECT
		"Hash_ID",
		"Created_Date",
		RAWTOHEX(STANDARD_HASH(CONCAT_STRING, ''MD5'')) AS "Hash_Summary"
	FROM temp_concat_strings
	WHERE RN = 1';

	DECLARE
		table_exists_3 NUMBER;
	BEGIN
		SELECT COUNT(*)
		INTO table_exists_3
		FROM user_tables
		WHERE table_name = 'TEMP_FINAL';

		IF table_exists_3 = 1 THEN
			EXECUTE IMMEDIATE 'TRUNCATE TABLE temp_final';
			EXECUTE IMMEDIATE 'DROP TABLE temp_final';
		END IF;
	END;

	EXECUTE IMMEDIATE
	'
	CREATE GLOBAL TEMPORARY TABLE temp_final
	ON COMMIT PRESERVE ROWS
	AS
	SELECT
		h."Hash_ID",
		h."Player",
		h."Nation",
		h."Position",
		h."Squad",
		h."Age",
		h."Birth_Year",
		h."Matches_Played",
		h."Starts",
		h."Minutes_Played",
		h."Minutes_90s",
		h."Goals",
		h."Assists",
		h."Goals_Plus_Assists",
		h."Goals_Excluding_PK",
		h."Penalty_Kicks",
		h."Penalty_Kicks_Attempted",
		h."Yellow_Cards",
		h."Red_Cards",
		h."Expected_Goals",
		h."NonPenalty_Expected_Goals",
		h."Expected_Assists",
		h."NonPenalty_Expected_Goals_Plus_Assists",
		h."Progressive_Carries",
		h."Progressive_Passes",
		h."Progressive_Receptions",
		h."Goals_Per_90_Minutes",
		h."Assists_Per_90_Minutes",
		h."Goals_Plus_Assists_Per_90_Minutes",
		h."Goals_Excluding_PK_Per_90_Minutes",
		h."Goals_Plus_Assists_Excluding_PK",
		h."Expected_Goals_Per_90_Minutes",
		h."Expected_Assists_Per_90_Minutes",
		h."Expected_Goals_Plus_Assists_Per_90_Minutes",
		h."NonPenalty_Expected_Goals_Per_90_Minutes",
		h."NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes",
		h."Created_Date",
		th."Hash_Summary"
	FROM FOOTSTATS.FOOTSTATS_HISTORY_PLAYERSTATS_BRASILEIRAO h
	INNER JOIN temp_hash th ON th."Hash_ID" = h."Hash_ID" 
	WHERE NOT EXISTS 
	(
		SELECT
			1
		FROM 
			FOOTSTATS.FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO f
		WHERE f."Hash_Summary" = th."Hash_Summary"
	)
	AND TRUNC(h."Created_Date") = TRUNC(SYSDATE)';

	EXECUTE IMMEDIATE 
	'
	MERGE INTO FOOTSTATS.FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO dst
	USING temp_final src
	ON 
	(
		dst."Player" = src."Player" 
		AND dst."Birth_Year" = src."Birth_Year" 
		AND dst."Squad" = src."Squad"
	)
	WHEN MATCHED THEN
		UPDATE SET
			dst."Nation" = src."Nation",
			dst."Age" = src."Age",
			dst."Position" = src."Position",
			dst."Matches_Played" = src."Matches_Played",
			dst."Starts" = src."Starts",
			dst."Minutes_Played" = src."Minutes_Played",
			dst."Minutes_90s" = src."Minutes_90s",
			dst."Goals" = src."Goals",
			dst."Assists" = src."Assists",
			dst."Goals_Plus_Assists" = src."Goals_Plus_Assists",
			dst."Goals_Excluding_PK" = src."Goals_Excluding_PK",
			dst."Penalty_Kicks" = src."Penalty_Kicks",
			dst."Penalty_Kicks_Attempted" = src."Penalty_Kicks_Attempted",
			dst."Yellow_Cards" = src."Yellow_Cards",
			dst."Red_Cards" = src."Red_Cards",
			dst."Expected_Goals" = src."Expected_Goals",
			dst."NonPenalty_Expected_Goals" = src."NonPenalty_Expected_Goals",
			dst."Expected_Assists" = src."Expected_Assists",
			dst."NonPenalty_Expected_Goals_Plus_Assists" = src."NonPenalty_Expected_Goals_Plus_Assists",
			dst."Progressive_Carries" = src."Progressive_Carries",
			dst."Progressive_Passes" = src."Progressive_Passes",
			dst."Progressive_Receptions" = src."Progressive_Receptions",
			dst."Goals_Per_90_Minutes" = src."Goals_Per_90_Minutes",
			dst."Assists_Per_90_Minutes" = src."Assists_Per_90_Minutes",
			dst."Goals_Plus_Assists_Per_90_Minutes" = src."Goals_Plus_Assists_Per_90_Minutes",
			dst."Goals_Excluding_PK_Per_90_Minutes" = src."Goals_Excluding_PK_Per_90_Minutes",
			dst."Goals_Plus_Assists_Excluding_PK" = src."Goals_Plus_Assists_Excluding_PK",
			dst."Expected_Goals_Per_90_Minutes" = src."Expected_Goals_Per_90_Minutes",
			dst."Expected_Assists_Per_90_Minutes" = src."Expected_Assists_Per_90_Minutes",
			dst."Expected_Goals_Plus_Assists_Per_90_Minutes" = src."Expected_Goals_Plus_Assists_Per_90_Minutes",
			dst."NonPenalty_Expected_Goals_Per_90_Minutes" = src."NonPenalty_Expected_Goals_Per_90_Minutes",
			dst."NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes" = src."NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes",
			dst."Hash_ID" = src."Hash_ID",
			dst."Hash_Summary" = src."Hash_Summary"
	WHEN NOT MATCHED THEN
		INSERT (
			"Player",
			"Nation",
			"Position",
			"Squad",
			"Age",
			"Birth_Year",
			"Matches_Played",
			"Starts",
			"Minutes_Played",
			"Minutes_90s",
			"Goals",
			"Assists",
			"Goals_Plus_Assists",
			"Goals_Excluding_PK",
			"Penalty_Kicks",
			"Penalty_Kicks_Attempted",
			"Yellow_Cards",
			"Red_Cards",
			"Expected_Goals",
			"NonPenalty_Expected_Goals",
			"Expected_Assists",
			"NonPenalty_Expected_Goals_Plus_Assists",
			"Progressive_Carries",
			"Progressive_Passes",
			"Progressive_Receptions",
			"Goals_Per_90_Minutes",
			"Assists_Per_90_Minutes",
			"Goals_Plus_Assists_Per_90_Minutes",
			"Goals_Excluding_PK_Per_90_Minutes",
			"Goals_Plus_Assists_Excluding_PK",
			"Expected_Goals_Per_90_Minutes",
			"Expected_Assists_Per_90_Minutes",
			"Expected_Goals_Plus_Assists_Per_90_Minutes",
			"NonPenalty_Expected_Goals_Per_90_Minutes",
			"NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes",
			"Created_Date",
			"Modified_Date",
			"Hash_ID",
			"Hash_Summary"
		)
		VALUES (
			src."Player",
			src."Nation",
			src."Position",
			src."Squad",
			src."Age",
			src."Birth_Year",
			src."Matches_Played",
			src."Starts",
			src."Minutes_Played",
			src."Minutes_90s",
			src."Goals",
			src."Assists",
			src."Goals_Plus_Assists",
			src."Goals_Excluding_PK",
			src."Penalty_Kicks",
			src."Penalty_Kicks_Attempted",
			src."Yellow_Cards",
			src."Red_Cards",
			src."Expected_Goals",
			src."NonPenalty_Expected_Goals",
			src."Expected_Assists",
			src."NonPenalty_Expected_Goals_Plus_Assists",
			src."Progressive_Carries",
			src."Progressive_Passes",
			src."Progressive_Receptions",
			src."Goals_Per_90_Minutes",
			src."Assists_Per_90_Minutes",
			src."Goals_Plus_Assists_Per_90_Minutes",
			src."Goals_Excluding_PK_Per_90_Minutes",
			src."Goals_Plus_Assists_Excluding_PK",
			src."Expected_Goals_Per_90_Minutes",
			src."Expected_Assists_Per_90_Minutes",
			src."Expected_Goals_Plus_Assists_Per_90_Minutes",
			src."NonPenalty_Expected_Goals_Per_90_Minutes",
			src."NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes",
			src."Created_Date",
			CURRENT_TIMESTAMP AT TIME ZONE ''UTC'',
			src."Hash_ID",
			src."Hash_Summary"
		)';

	EXECUTE IMMEDIATE 'TRUNCATE TABLE temp_concat_strings';
	EXECUTE IMMEDIATE 'DROP TABLE temp_concat_strings';
	EXECUTE IMMEDIATE 'TRUNCATE TABLE temp_hash';
	EXECUTE IMMEDIATE 'DROP TABLE temp_hash';
	EXECUTE IMMEDIATE 'TRUNCATE TABLE temp_final';
	EXECUTE IMMEDIATE 'DROP TABLE temp_final';

END;

/

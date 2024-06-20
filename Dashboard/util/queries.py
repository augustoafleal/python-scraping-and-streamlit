select_logs = """
                SELECT * FROM 
                (
                    SELECT process_date, processed_rows, processed_columns, script_file, table_loaded
                    FROM footstats_logs fl
                    WHERE TRUNC(process_date) >= TRUNC(SYSDATE - 5) 
                    ORDER BY process_date DESC
                ) 
                WHERE ROWNUM <= 5 
                """

select_goals = """
                SELECT
                    "Player", "Squad", "Goals", "Position", "Nation"
                FROM footstats_summary_playerstats_brasileirao
                """

select_minutes_all = """
                    SELECT 
                        "Squad", "Player", "Starts", "Minutes_Played"
                    FROM footstats_summary_playerstats_brasileirao
                    """

select_squads = """
                    SELECT 
                        DISTINCT "Squad"
                    FROM footstats_summary_playerstats_brasileirao
                """

select_player = """
                    SELECT 
                        *
                    FROM footstats_summary_playerstats_brasileirao
                    WHERE "Squad" = :squad
                    AND "Player" LIKE :player
                """

select_player_history = """
                            SELECT
                                * 
                            FROM
                            (
                                SELECT
                                "Player",
                                "Squad",
                                "Minutes_Played",
                                "Goals",
                                "Assists",
                                TO_CHAR("Created_Date", 'YYYY-MM-DD') AS "Created_Date",
                                ROW_NUMBER() OVER (PARTITION BY "Player",  "Squad", "Minutes_Played", "Goals", "Assists" ORDER BY "Created_Date" ASC) AS RN
                                FROM FOOTSTATS_HISTORY_PLAYERSTATS_BRASILEIRAO
                                WHERE "Squad" = :squad
                                AND "Player" LIKE :player
                                ORDER BY "Created_Date" DESC
                            )
                            WHERE RN = 1
                        """

select_squad_players_count = """
                                SELECT
                                    COUNT("Player") AS "Players",
                                    "Squad"
                                FROM FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO
                                GROUP BY "Squad" 
                                ORDER BY "Squad"
                            """

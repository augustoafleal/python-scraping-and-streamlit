CREATE TABLE "FOOTSTATS"."FOOTSTATS_LOGS" 
(	
    "PROCESSED_ROWS" NUMBER(*,0), 
	"PROCESSED_COLUMNS" NUMBER(*,0), 
	"SCRIPT_FILE" VARCHAR2(250 BYTE) COLLATE "USING_NLS_COMP", 
	"TABLE_LOADED" VARCHAR2(250 BYTE) COLLATE "USING_NLS_COMP", 
	"PROCESS_DATE" TIMESTAMP (6)
)  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
TABLESPACE "DATA" ;

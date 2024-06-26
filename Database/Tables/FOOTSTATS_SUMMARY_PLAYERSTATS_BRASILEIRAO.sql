CREATE TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" 
(	
	"Player" VARCHAR2(255 BYTE) COLLATE "USING_NLS_COMP", 
	"Nation" VARCHAR2(255 BYTE) COLLATE "USING_NLS_COMP", 
	"Position" VARCHAR2(50 BYTE) COLLATE "USING_NLS_COMP", 
	"Squad" VARCHAR2(255 BYTE) COLLATE "USING_NLS_COMP", 
	"Age" NUMBER(*,0), 
	"Birth_Year" NUMBER(*,0), 
	"Matches_Played" NUMBER(*,0), 
	"Starts" NUMBER(*,0), 
	"Minutes_Played" NUMBER(*,0), 
	"Minutes_90s" NUMBER(5,2), 
	"Goals" NUMBER(*,0), 
	"Assists" NUMBER(*,0), 
	"Goals_Plus_Assists" NUMBER(*,0), 
	"Goals_Excluding_PK" NUMBER(*,0), 
	"Penalty_Kicks" NUMBER(*,0), 
	"Penalty_Kicks_Attempted" NUMBER(*,0), 
	"Yellow_Cards" NUMBER(*,0), 
	"Red_Cards" NUMBER(*,0), 
	"Expected_Goals" NUMBER(5,2), 
	"NonPenalty_Expected_Goals" NUMBER(5,2), 
	"Expected_Assists" NUMBER(5,2), 
	"NonPenalty_Expected_Goals_Plus_Assists" NUMBER(5,2), 
	"Progressive_Carries" NUMBER(*,0), 
	"Progressive_Passes" NUMBER(*,0), 
	"Progressive_Receptions" NUMBER(*,0), 
	"Goals_Per_90_Minutes" NUMBER(5,2), 
	"Assists_Per_90_Minutes" NUMBER(5,2), 
	"Goals_Plus_Assists_Per_90_Minutes" NUMBER(5,2), 
	"Goals_Excluding_PK_Per_90_Minutes" NUMBER(5,2), 
	"Goals_Plus_Assists_Excluding_PK" NUMBER(5,2), 
	"Expected_Goals_Per_90_Minutes" NUMBER(5,2), 
	"Expected_Assists_Per_90_Minutes" NUMBER(5,2), 
	"Expected_Goals_Plus_Assists_Per_90_Minutes" NUMBER(5,2), 
	"NonPenalty_Expected_Goals_Per_90_Minutes" NUMBER(5,2), 
	"NonPenalty_Expected_Goals_Plus_Assists_Per_90_Minutes" NUMBER(5,2), 
	"Created_Date" DATE DEFAULT CURRENT_DATE, 
	"Modified_Date" TIMESTAMP (6), 
	"Hash_ID" RAW(16), 
	"Hash_Summary" RAW(16)
)  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
	PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
	STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
	PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
	BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
	TABLESPACE "DATA" ;

CREATE UNIQUE INDEX "FOOTSTATS"."SYS_C0031894" ON "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" ("Player", "Birth_Year", "Squad") 
PCTFREE 10 INITRANS 20 MAXTRANS 255 COMPUTE STATISTICS 
STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
TABLESPACE "DATA" ;


ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Player" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Nation" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Position" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Squad" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Age" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Created_Date" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" MODIFY ("Modified_Date" NOT NULL ENABLE);
ALTER TABLE "FOOTSTATS"."FOOTSTATS_SUMMARY_PLAYERSTATS_BRASILEIRAO" ADD PRIMARY KEY ("Player", "Birth_Year", "Squad")
USING INDEX PCTFREE 10 INITRANS 20 MAXTRANS 255 COMPUTE STATISTICS 
STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
TABLESPACE "DATA"  ENABLE;

/*=======================================================================================
** File Name:  sch_tblidx.h
**
** Title:  Table indicies into the CFS scheduler's message table for CFS653 mission
**
** $Author:    Auto-generated by Python script
** $Revision:  $
** $Date:      2013-01-16
**
** Purpose:  This header file contains table indicies into the message table.
**
**=====================================================================================*/

#ifndef _SCH_TBL_IDX_H_
#define _SCH_TBL_IDX_H_

/*
** Pragmas
*/

/*
** Include Files
*/

/*
** Local Defines
*/
#define CFE_ES_SEND_HK_MIDX    		1
#define CFE_EVS_SEND_HK_MIDX   		2
#define CFE_SB_SEND_HK_MIDX    		3
#define CFE_TIME_SEND_HK_MIDX  		4
#define CFE_TBL_SEND_HK_MIDX   		5
#define CFE_TIME_FAKE_CMD_MIDX		6
#define SCH_SEND_HK_MIDX       		15
#define TO_SEND_HK_MIDX				16
#define HK_SEND_HK_MIDX       		17
#define TO_SEND_TLM_MIDX			19
#define HK_SEND_COMBINED_PKT1_MIDX	20
#define HK_SEND_COMBINED_PKT2_MIDX	21
#define HK_SEND_COMBINED_PKT3_MIDX	22
#define HK_SEND_COMBINED_PKT4_MIDX	23
#define HK_SEND_COMBINED_PKT5_MIDX	24
#define HK_SEND_COMBINED_PKT6_MIDX	25
#define HK_SEND_COMBINED_PKT7_MIDX	26
#define HK_SEND_COMBINED_PKT8_MIDX	27
#define HK_SEND_COMBINED_PKT9_MIDX	28
#define HK_SEND_COMBINED_PKT10_MIDX	29

#define FM_SEND_HK_MIDX				30
#define LC_SEND_HK_MIDX				31
#define HS_WAKEUP_MIDX 				32
#define HS_SEND_HK_MIDX				33
#define MD_SEND_HK_MIDX				34
#define MD_WAKEUP_MIDX 				35
#define DS_SEND_HK_MIDX				37
#define CS_SEND_HK_MIDX				38
#define CS_BACKGROUND_CYCLE_MIDX 	39
#define SC_1HZ_WAKEUP_MIDX			40
#define SC_SEND_HK_MIDX				41

#define VC_SEND_HK_MIDX				46
#define VC_WAKEUP_MIDX				47

#define CI_READ_CMD_MIDX			50

#define CI_SEND_HK_MIDX             53
#define CF_SEND_HK_MIDX				57
#define CF_WAKE_UP_REQ_CMD_MIDX		58

#define MM_SEND_HK_MIDX				70

#define MPU9250_SEND_HK_MIDX		72
#define MPU9250_MEASURE_MIDX		73

#define MS5611_SEND_HK_MIDX			76
#define MS5611_MEASURE_MIDX			77

#define NEOM8N_SEND_HK_MIDX			85
#define NEOM8N_MEASURE_MIDX			86
#define NEOM8N_PROC_CMDS_MIDX		87

#define PX4BR_PROC_CMD_MIDX			100
#define PX4BR_SEND_HK_MIDX			101

#define CFE_TIME_TONE_CMD_MIDX		110
#define CFE_TIME_1HZ_CMD_MIDX		111

#define EA_WAKEUP_MIDX 				125
#define EA_PERFMON_MIDX 			126
#define EA_SEND_HK_MIDX 			127

#endif /* _SCH_TBL_IDX_H_ */

/*=======================================================================================
** End of file sch_tblidx.h
**=====================================================================================*/
    

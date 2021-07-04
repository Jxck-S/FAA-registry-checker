# FAA-registry-checker
Checks FAA Registry daily for new aircraft registered by certain owners as configured.

Currently only searches for new aircraft by owner/registry name but plan to add more features like deregister, detect update to registration, and N-Number reserve.

Configure in ./configs/mainconf.ini
Currently outputs to terminal and Discord if configured w/ webhook. 

Example of program running
```
-------- 0 -------- 11:00:41 PM --------------------------------------------------------------------
Already have FAA_Reg_DB_Latest.zip deleting and redownloading
Successfully got FAA_Reg_DB_Latest.zip
1851 Current Regs in searched names
-------- 1 -------- 11:00:41 PM ------------------------Elapsed Time- 12.764 -----------------------
Sleeping till 2021-07-01 05:00:00+00:00
-------- 1 -------- 11:00:41 PM --------------------------------------------------------------------
Already have FAA_Reg_DB_Latest.zip deleting and redownloading
Successfully got FAA_Reg_DB_Latest.zip
Found new reg for BANK OF UTAH TRUSTEE N296NV a AIRBUS A320-214 https://registry.faa.gov/aircraftinquiry/Search/NNumberResult?NNumbertxt=296NV
Found new reg for BANK OF UTAH TRUSTEE N876GJ a BELL HELICOPTER TEXTRON CANADA 407 https://registry.faa.gov/aircraftinquiry/Search/NNumberResult?NNumbertxt=876GJ
Found new reg for BANK OF UTAH TRUSTEE N89NC a GULFSTREAM AEROSPACE CORP GVII-G600 https://registry.faa.gov/aircraftinquiry/Search/NNumberResult?NNumbertxt=89NC
1854 Current Regs in searched names
-------- 2 -------- 11:00:41 PM ------------------------Elapsed Time- 11.219 -----------------------
Sleeping till 2021-07-02 05:00:00+00:00
-------- 2 -------- 11:00:41 PM --------------------------------------------------------------------
Already have FAA_Reg_DB_Latest.zip deleting and redownloading
Successfully got FAA_Reg_DB_Latest.zip
Found new reg for BANK OF UTAH TRUSTEE N228JV a TEXTRON AVIATION INC 560XL https://registry.faa.gov/aircraftinquiry/Search/NNumberResult?NNumbertxt=228JV
Found new reg for BANK OF UTAH TRUSTEE N578GJ a BOMBARDIER INC CL-600-2C10 https://registry.faa.gov/aircraftinquiry/Search/NNumberResult?NNumbertxt=578GJ
1856 Current Regs in searched names
-------- 3 -------- 11:00:41 PM ------------------------Elapsed Time- 30.341 -----------------------
Sleeping till 2021-07-03 05:00:00+00:00
```

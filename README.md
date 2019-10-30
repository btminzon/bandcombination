This script is intended to parse UE Capability Information message, from Wireshark,  Qualcomm and Infovista's TEMS format.

It will extract some information and show an Excel table in a friendly format.

So far, it is parsing:
1) Supported Bands
2) Bandwidth Class
3) MIMO information
4) Total number of layers in a band combination
5) Bandwidth Combination Set (BCS)
6) 256QAM in DL and 64QAM in UL support
7) B66, LAA and LTE-U bands

to run, there are two options: command line or using an UI:
1) python UECapabilityInformationPaser.py (option) (UECapabilityInformation file in text format)
   * options available:
       --help    | -h  --> Show help
       --output  | -o  --> Store output file in output folder

2) python UECapabilityInformationPaser.py
   Running without any parameters will open a window, where one can paste a UECapabilityInformation and click on Parse
   button to parse. It will generate UeCapabilityInformation.xlsx as output

Any comment or suggestion, feel free to contact me or create a new branch with the changes!
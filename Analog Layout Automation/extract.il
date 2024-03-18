cv=dbOpenCellViewByType("bye" "all" "schematic" "schematic" "r")
lay = deNewCellView("bye", "all", "layout", "maskLayout", nil))
layout_view = dbOpenCellViewByType("bye", "all", "layout", "maskLayout", w))

; Wires' width calculations 
;################################
;Yasser's Constants
current_capability = 1.8
;Input_current = 0.36
Input_current = 2.1 ; max

Input_pwr_grid = 8
pwr_grid_Width= Input_pwr_grid/current_capability

tf=techGetTechFile(cv)
schCv = dbOpenCellViewByType(cv~>libName cv~>cellName "schematic" "" "a")


dbSave(layout_view)
flag_d = 1 
flag_s = 1
flag_g = 1
flag_g2 = 1
flag_x = 1
flag_stacking = 1
bool_G_P=1

/*###########################
Different Technologies
#############################*/
foreach( inst schCv~>instances 
if( inst~>purpose != "pin" then 
technology=inst~>master~>view~>lib~>name
NMOS=inst~>master~>view~>cell~>name
printf("technology %L\n" technology)
)
)

/*###########TSMC##############*/
if(technology == "tsmcN65" then
M1Holder="M1" 
M2Holder="M2" 
M3Holder="M3" 
M4Holder="M4" 
M5Holder="M5" 
via21Holder="M2_M1" 
via32Holder="M3_M2" 
via43Holder="M4_M3" 
via54Holder="M5_M4"
M1NwHolder="M1_NW"
M1SUbHolder="M1_SUB"  
NwHolder="NW" 
minSpHolder="minSameNetSpacing"
min_device_spacing= techGetSpacingRule(tf "minSpacing" "DCO" "NW")
sdHolder="sd"
rouPolHolder="routePolydir" 
refHolder="ref"
simHolder="simM" 
wHolder="w" 
wfHolder="wf"
PPHolder="PP"
NPHolder= "NP"
saHolder="sa"

)
/*########### GPDK ##############*/

if(technology == "gpdk090" then
M1Holder="Metal1" 
M2Holder="Metal2" 
M3Holder="Metal3" 
M4Holder="Metal4" 
M5Holder="Metal5" 
via21Holder="M2_M1v" 
via32Holder="M3_M2v" 
via43Holder="M4_M3v" 
via54Holder="M5_M4v" 	
M1NwHolder="M1_NWELL" 
M1SUbHolder="M1_PSUB" 
NwHolder="Nwell" 
minSpHolder="minDiagonalSpacing"
min_device_spacing= techGetSpacingRule(tf "minSpacing" "Nimp")
sdHolder="sdMtlWidth"
rouPolHolder="connectGates" 
refHolder="text"
simHolder="m" 
wHolder="fw" 
wfHolder="w"
PPHolder="Pimp"
NPHolder="Nimp"
saHolder="sdMtlWidth"
 )

/*########### UMC ##############*/
if( technology == "umc13mmrf" then 

M1Holder="ME1"
M2Holder="ME2"
M3Holder="ME3"
M4Holder="ME4"
M5Holder="ME5"
via21Holder="M2_M1" 
via32Holder="M3_M2" 
via43Holder="M4_M3" 
via54Holder="M5_M4"
M1NwHolder="M1_NWEL" 
M1SUbHolder="M1_PSUB" 
NwHolder="NWEL" 
minSpHolder="minSpacing"
min_device_spacing= techGetSpacingRule(tf "minSpacing" "minWidth" "NWEL")
sdHolder="sdMtlWidth"
rouPolHolder="connectGates"
refHolder="DIFF"
simHolder="simM" 
wHolder="w" 
wfHolder="wf"
PPHolder="PP"
NPHolder="SUBSTRATE"
saHolder="sdMtlWidth"
)

/*##################################################################*/

min_spacing_M5=techGetSpacingRule(tf minSpHolder M5Holder)
min_spacing_M4=techGetSpacingRule(tf minSpHolder M4Holder)
min_spacing_M3=techGetSpacingRule(tf minSpHolder M3Holder)
min_spacing_M2=techGetSpacingRule(tf minSpHolder M2Holder)

min_Width_M1=techGetSpacingRule(tf "minWidth" M1Holder)
max_Width_M1=techGetSpacingRule(tf "maxWidth" M1Holder)

min_Width_M2=techGetSpacingRule(tf "minWidth" M2Holder)
max_Width_M2=techGetSpacingRule(tf "maxWidth" M2Holder)

min_Width_M3=techGetSpacingRule(tf "minWidth" M3Holder)
;max_Width_M3= techGetSpacingRule(tf "maxWidth" M3Holder)/12
max_Width_M3= 1
Opt_Width_M3=round(techGetSpacingRule(tf "minWidth" M3Holder)*1.4/0.01)*0.01

min_Width_M4=techGetSpacingRule(tf "minWidth" M4Holder)
max_Width_M4=techGetSpacingRule(tf "maxWidth" M4Holder)

min_Width_M5=techGetSpacingRule(tf "minWidth" M5Holder)
max_Width_M5=techGetSpacingRule(tf "maxWidth" M5Holder)

;DETERMINING THE WIRES WIDTH ACCORDING TO THE SOURCE CURRENT AND THE WIRES CURRENT CAPABILITY 
;Input_current = 3
; reads the constraints of the drm
;current_capability= nth(2 techGetCurrentDensityRuleTable(tf "rmsACCurrentDensity" M3Holder))
;M3_corr_width=car(last(nth(1 techGetCurrentDensityRuleTable(tf "rmsACCurrentDensity" M3Holder))))
;source_Width_H = Input_current*M3_corr_width / current_capability
source_Width_H = Input_current/current_capability
if(source_Width_H<techGetSpacingRule(tf "minWidth" M3Holder) then source_Width_H=techGetSpacingRule(tf "minWidth" M3Holder) )

;Stacking for source_Width_H 
if(source_Width_H<=max_Width_M3 then
	source_Width_H = round(source_Width_H/0.01)*0.01
else
	if(source_Width_H>max_Width_M3 then 
		source_Width_H= round((source_Width_H/2)/0.01)*0.01
	flag_stacking= 0
	)	
)	
if(source_Width_H>=min_Width_M3 && source_Width_H< 0.2 then DRC_space_stack= min_spacing_M3  DRC_Width= min_Width_M3)
if(source_Width_H>=0.2 && source_Width_H< 0.4 then DRC_space_stack= 0.12  DRC_Width= 0.2)
if(source_Width_H>=0.4 && source_Width_H< 1.5 then DRC_space_stack= 0.16 DRC_Width= 0.4)	
if(source_Width_H>=1.5 && source_Width_H< 4.5 then DRC_space_stack= 0.5 DRC_Width= 1.5)
if(source_Width_H>=4.5 then DRC_space_stack= 1.5 DRC_Width= 4.5)

Upper_space_NCM= 4*source_Width_H+5*DRC_space_stack*1.4
Lower_space_NCM= (source_Width_H+2*DRC_space_stack*1.4+Opt_Width_M3)
Upper_space_PCM= (source_Width_H+2*DRC_space_stack*1.4+Opt_Width_M3) 
Lower_space_PCM= 3*(source_Width_H+DRC_space_stack*1.4)
upper_space_n_diff_pair= 2*(source_Width_H+DRC_space_stack*1.4)
lower_space_n_diff_pair= source_Width_H+DRC_space_stack*1.4
Middle_space_n_diff_pair= 2*min_Width_M3 + 2*(min_Width_M3 *1.4) +7*min_spacing_M3*1.4
upper_space_p_Load= (3*source_Width_H+4*DRC_space_stack*1.4)+Opt_Width_M3
lower_space_p_Load= 2*(source_Width_H+DRC_space_stack*1.4)
upper_space_n_Load= 2*(source_Width_H+DRC_space_stack*1.4)
lower_space_n_Load= (source_Width_H+2*DRC_space_stack*1.4+Opt_Width_M3)
Space_btw_diff_and_pmos= 2*(source_Width_H+DRC_space_stack*1.4)
V_channel=source_Width_H+2*(DRC_space_stack*1.4)

;################################
; EXTRACT THE NETLIST 
;################################


myPort = outfile("./netlist.txt")
foreach( inst schCv~>instances
if(inst~>purpose != "pin" then
;printf("inst:%s %L\n" inst~>name inst~>prop~>name)
fprintf(myPort "%s %L %L %L" inst~>name inst~>conns~>net~>name inst~>master~>view~>lib~>name inst~>master~>view~>cell~>name)
m_indx=-1
simM_indx=-1
cdf=cdfGetInstCDF(inst) ; Cdf:componet description format  https://www.edaboard.com/threads/whats-cdf-of-cadence-whats-usage-tks.33063/
foreach( param cdf->parameters
;println(prop~>name)
 when( param~>name ==wHolder w_indx=lindex(cdf->parameters~>name wHolder))
 when( param~>name =="l" l_indx=lindex(cdf->parameters~>name "l"))
 when( param~>name =="as" as_indx=lindex(cdf->parameters~>name "as"))
 when( param~>name =="ad" ad_indx=lindex(cdf->parameters~>name "ad"))
 when( param~>name =="ps" ps_indx=lindex(cdf->parameters~>name "ps"))
 when( param~>name =="pd" pd_indx=lindex(cdf->parameters~>name "pd"))
 when( param~>name =="m" m_indx=lindex(cdf->parameters~>name "m")) 
 when( param~>name ==saHolder sa_indx=lindex(cdf->parameters~>name saHolder) sa= nth(sa_indx-1 cdf->parameters~>value))
 when( param~>name ==simHolder simM_indx=lindex(cdf->parameters~>name simHolder))
 when( param~>name =="fingers" fingers_indx=lindex(cdf->parameters~>name "fingers") fingers_value=nth(fingers_indx-1 cdf->parameters~>value))
 if(not(member("fingers" cdf->parameters~>name)) then fingers_value=1)
 when(param~>name == sdHolder sd_indx=lindex(cdf~>parameters~>name sdHolder) sd=nth(sd_indx-1 cdf->parameters~>value))
      )
; getting the max W/L
max_WperL=-1
printf("l_indx %L nth(l_indx-1 cdf~>parameters~>value) %L \n" l_indx nth(l_indx-1 cdf~>parameters~>value) )
printf("w_indx %L nth(w_indx-1 cdf~>parameters~>value) %L \n" w_indx nth(w_indx-1 cdf~>parameters~>value) )

if((aelNumber(nth(w_indx-1 cdf->parameters~>value))/aelNumber("1u"))/(aelNumber(nth(l_indx-1 cdf~>parameters~>value))/aelNumber("1u")) > max_WperL then 
max_WperL=(aelNumber(nth(w_indx-1 cdf->parameters~>value))/aelNumber("1u"))/(aelNumber(nth(l_indx-1 cdf->parameters~>value))/aelNumber("1u"))
inst_ID= inst
)
if(technology=="tsmcN65" then
spacing=(aelNumber(sd)*0.001)/aelNumber("1n")
)
if(technology=="gpdk090" then
sa= ((aelNumber(sa)/aelNumber("1u"))+.16)*aelNumber("1u")
sa=aelSuffixNotation(sa)
sd= ((aelNumber(sd)/aelNumber("1u"))+.2)*aelNumber("1u")
spacing=(aelNumber(sd)*0.001)/aelNumber("1n")
sd=aelSuffixNotation(sd)

)
if(technology=="umc13mmrf" || technology=="umc90mmrf" then
sa= ((aelNumber(sa)/aelNumber("1u"))+.16)*aelNumber("1u")
sa=aelSuffixNotation(sa)
sd= ((aelNumber(sd)/aelNumber("1u"))+.2)*aelNumber("1u")
spacing=(aelNumber(sd)*0.001)/aelNumber("1n")
sd=aelSuffixNotation(sd)
)
fprintf(myPort " w=%L L=%L fingers=%L as=%L ad=%L ps=%L pd=%L sd=%L sa=%L m=%L simM=%L\n" nth(w_indx-1 cdf->parameters~>value) nth(l_indx-1 cdf->parameters~>value) fingers_value nth(as_indx-1 cdf->parameters~>value) nth(ad_indx-1 cdf->parameters~>value) nth(ps_indx-1 cdf->parameters~>value) nth(pd_indx-1 cdf->parameters~>value) sd sa nth(m_indx-1 cdf->parameters~>value) nth(simM_indx-1 cdf->parameters~>value)) 
)
)

;CREATING A DUMMY TO GET THE DIFFERENCE BETWEEN THE Bbox  AND THE LENGTH AND WIDTH
DUMMY=dbCreateInstByMasterName(layout_view technology NMOS "layout" "Dummy" list(0 0) "R0") ; CREATING INSTANCES AT THE SPECIFIED LOCATION 
	
cdf=cdfGetInstCDF(DUMMY) ; Cdf:componet description format  https://www.edaboard.com/threads/whats-cdf-of-cadence-whats-usage-tks.33063/
      foreach( param cdf~>parameters
      sch_params=cdfGetInstCDF(inst_ID)~>parameters
      foreach( sch_param sch_params
		if(sch_param~>name == param~>name && param~>name !="fingers" then
			 param~>value =sch_param~>value
			 )
		if(param~>name == "l" then
			length = param~>value
			length_micro= aelNumber(length)/aelNumber("1u")
			)
		if(param~>name == wHolder then
			width = param~>value
			width_micro = aelNumber(width)/aelNumber("1u")
		)	  
		)
      )
V_difference= (yCoord(car(cdr(DUMMY~>bBox)))-yCoord(car(DUMMY~>bBox))-width_micro)/2
dbCreateProp(DUMMY rouPolHolder "string" "Top") 
dbCreateProp(DUMMY "polyContacts" "boolean" t) 
V_difference_with_contact= yCoord(car(cdr(DUMMY~>bBox)))-yCoord(car(DUMMY~>bBox))-width_micro- V_difference

H_difference= (xCoord(car(cdr(DUMMY~>bBox)))-xCoord(car(DUMMY~>bBox))-length_micro)/2 
dbDeleteObject(DUMMY)        
; GETTING THE PINS NAMES 
foreach( terminal schCv~>terminals
	if(terminal~>name !="VDD" then
	fprintf(myPort "%s\n" terminal~>name)
	)
	)
fprintf(myPort "V_difference %n\nV_difference_with_contact %n\nH_difference %n\n" V_difference V_difference_with_contact H_difference)
fprintf(myPort "Upper_space_NCM %n\nLower_space_NCM %n\nUpper_space_PCM %n\nLower_space_PCM %n\nupper_space_n_diff_pair %n\nlower_space_n_diff_pair  %n\nupper_space_p_Load %n\nlower_space_p_Load %n\nupper_space_n_Load %n\nlower_space_n_Load %n\nmin_device_spacing %n\nMiddle_space_n_diff_pair %n\n" Upper_space_NCM Lower_space_NCM Upper_space_PCM Lower_space_PCM upper_space_n_diff_pair lower_space_n_diff_pair upper_space_p_Load lower_space_p_Load upper_space_n_Load lower_space_n_Load min_device_spacing Middle_space_n_diff_pair )
fprintf(myPort "Space_btw_diff_and_pmos %n\n" Space_btw_diff_and_pmos )
close( myPort )
myPort = nil

ciwHiExit()
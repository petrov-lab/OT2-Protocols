from opentrons import labware, instruments, robot

tiprack_200ul = labware.load('tiprack-200ul', '10')
tiprack_10ul = labware.load('tiprack-10ul', '11')

"""
Primer Tuberack in location 6.
Contains 2ml tubes with 'N' Nextera Primers. Order of use:
01   05   09   x   x   x
02   06   10   x   x   x
03   07   11   x   x   x
04   08   12   x   x   x

For Set D default with all primers used:

N716   N721   N726   x   x   x
N718   N722   N727   x   x   x
N719   N723   N728   x   x   x
N720   N724   N729   x   x   x

"""
tuberack_primers = labware.load('tube-rack-2ml', '6')


"""
DNA Tuberack in location 5.
Contains cleaned-up Step 1 PCR product in 2ml tubes. 
Order used:

01   05   09   13   17   21
02   06   10   14   18   22
03   07   11   15   19   23
04   08   12   16   20   24

"""
tuberack_DNA = labware.load('tube-rack-2ml', '5')


"""
MasterMix in 2ml tubes in location 4.
MM for first S primer in A1 (row 1, col 1).
MM for second S primer in B1 (row 2, col 1).
Contains Q5 Polymerase + Q5 Buffer + dNTP + Water + S Primer
"""
tuberack_MM = labware.load('tube-rack-2ml', '4')


"""
Output plate in location 1.
Ends up arrayed as:

01a   03a   05a   07a   09a   11a   13a   15a   17a   19a   21a   23a
01b   03b   05b   07b   09b   11b   13b   15b   17b   19b   21b   23b
01c   03c   05c   07c   09c   11c   13c   15c   17c   19c   21c   23c
x     x     x     x     x     x     x     x     x     x     x     x
02a   04a   06a   08a   10a   12a   14a   16a   18a   20a   22a   24a  
02b   04b   06b   08b   10b   12b   14b   16b   18b   20b   22b   24b
02c   04c   06c   08c   10c   12c   14c   16c   18c   20c   22c   24c
x     x     x     x     x     x     x     x     x     x     x     x

"""
output_plate = labware.load('96-PCR-tall', '1')


s300 = instruments.P300_Single(
    tip_racks=[tiprack_200ul],
    mount="right",
)

s10 = instruments.P10_Single(
    tip_racks=[tiprack_10ul],
    mount="left"
)

# add 12 primers ('N' Nextera Primers) to all 24 DNA tubes

for i in range(12):
    s10.transfer(6.25, tuberack_primers.wells(i), tuberack_DNA.wells(i), mix_before=(3, 5), new_tip='always')

for i in range(12):
    s10.transfer(6.25, tuberack_primers.wells(i), tuberack_DNA.wells(i+12), mix_before=(3, 5), new_tip='always')

# add MM to DNA tube, mix up and down, and transfer into 3 PCR rxns

for i in range(12):
    s300.pick_up_tip()
    s300.transfer(65.75, tuberack_MM.wells(0), tuberack_DNA.wells(i), mix_before=(3, 50), new_tip='never', mix_after=(5, 50))
    s300.aspirate(150,tuberack_DNA.wells(i))
    for j in range(3):
        s300.dispense(50,output_plate.wells((4*(i)+j)))
    s300.blow_out(output_plate.wells((4*(i)+j)))
    s300.drop_tip()

for i in range(12, 24):
    s300.pick_up_tip()
    s300.transfer(65.75, tuberack_MM.wells(1), tuberack_DNA.wells(i), mix_before=(3, 50), new_tip='never', mix_after=(5, 50))
    s300.aspirate(150,tuberack_DNA.wells(i))
    for j in range(3):
        s300.dispense(50,output_plate.wells((4*(i)+j)))
    s300.blow_out(output_plate.wells((4*(i)+j)))
    s300.drop_tip()








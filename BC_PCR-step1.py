from opentrons import labware, instruments, robot


tiprack_200ul = labware.load('tiprack-200ul', '10')
tiprack_10ul = labware.load('tiprack-10ul', '11')

"""
DNA Tuberack in location 4.
Contains genomic DNA in 2ml tubes. 
Order used:

01   05   09   13   17   21
02   06   10   14   18   22
03   07   11   15   19   23
04   08   12   16   20   24

"""
tuberack_DNA = labware.load('tube-rack-2ml', '4')


"""
Primer Tuberack in location 6.
Contains 2ml tubes with Step 1 Forward Primers. Order of use:
01   05   09
02   06   10
03   07   11
04   08   12

For default with all primers used:

F201   F205   F209   x   x   x
F202   F206   F210   x   x   x
F203   F207   F211   x   x   x
F204   F208   F212   x   x   x

"""
tuberack_primers = labware.load('tube-rack-2ml', '6')


"""
Mix Tuberack in location 5.
Empty tubes. MasterMix per sample is created in this tubes
"""
tuberack_mix = labware.load('tube-rack-2ml', '5')


"""
MasterMix in 50ml tubes in location 4.
MM for first reverse primer in A3.
MM for second reverse primer in A4.
Contains HotStartTaq, MgCl2, Water, Reverse Primer
"""
mm_tuberack = labware.load('tube-rack-15_50ml', '7')


"""
Output plates. 
Ends up with 8 reactions per sample arrayed as:

01a   02a   ...   12a
01b   02b   ...   12b
01c   02c   ...   12c
01d   02d   ...   12d
01e   02e   ...   12e 
01f   02f   ...   12f
01g   02g   ...   12g
01h   02h   ...   12h

"""
output_plate_1 = labware.load('96-PCR-tall', '1')
output_plate_2 = labware.load('96-PCR-tall', '2')

s300 = instruments.P300_Single(
    tip_racks=[tiprack_200ul],
    mount="right",
)

s10 = instruments.P10_Single(
    tip_racks=[tiprack_10ul],
    mount="left"
)

# distribute 320ul mastermix to first 12 mix tubes

s300.distribute(160, mm_tuberack['A3'], tuberack_mix.wells(0, to=11))
s300.distribute(160, mm_tuberack['A3'], tuberack_mix.wells(0, to=11))

# distribute 320ul mastermix to second 12 mix tubes

s300.distribute(160, mm_tuberack['A4'], tuberack_mix.wells(12, to=23))
s300.distribute(160, mm_tuberack['A4'], tuberack_mix.wells(12, to=23))

# add 12 primers to all 24 mix tubes

for i in range(12):
	s10.transfer(8, tuberack_primers.wells(i), tuberack_mix.wells(i), mix_before=(3, 5), new_tip='always')

for i in range(12):
	s10.transfer(8, tuberack_primers.wells(i), tuberack_mix.wells(i+12), mix_before=(3, 5), new_tip='always')

# add 24 sample DNA to all 24 mix tubes, then add to PCR plate with the same pipette tip

for i in range(12):
    s300.pick_up_tip()
    s300.transfer(72, tuberack_DNA.wells(i), tuberack_mix.wells(i), mix_before=(3, 50), new_tip='never', mix_after=(5, 50))
    s300.aspirate(200,tuberack_mix.wells(i))
    for j in range(4):
        s300.dispense(50,output_plate_1.wells(8*(i)+j))
    s300.blow_out(output_plate_1.wells(8*(i)+j))
    s300.aspirate(200,tuberack_mix.wells(i))
    for j in range(4,8):
        s300.dispense(50,output_plate_1.wells(8*(i)+j))
    s300.blow_out(output_plate_1.wells(8*(i)+j))
    s300.drop_tip()

    # s300.distribute(50, tuberack_mix.wells(i), output_plate_1.wells((8*(i)), to=((8*i)+(7)))) old way of doing it - but dripped


for i in range(12, 24):
    s300.pick_up_tip()
    s300.transfer(72, tuberack_DNA.wells(i), tuberack_mix.wells(i), mix_before=(3, 50), new_tip='never', mix_after=(5, 50))
    s300.aspirate(200,tuberack_mix.wells(i))
    for j in range(4):
        s300.dispense(50,output_plate_2.wells(8*(i-12)+j))
    s300.blow_out(output_plate_2.wells(8*(i-12)+j))
    s300.aspirate(200,tuberack_mix.wells(i))
    for j in range(4,8):
        s300.dispense(50,output_plate_2.wells(8*(i-12)+j))
    s300.blow_out(output_plate_2.wells(8*(i-12)+j))
    s300.drop_tip()

    # s300.distribute(50, tuberack_mix.wells(i), output_plate_2.wells((8*(i-12)), to=((8*(i-12))+7))) old way of doing it - but dripped









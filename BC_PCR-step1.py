from opentrons import labware, instruments, robot

# single p300, single p10
# tip rack for both pipettes
# 3x tube rack 2ml
# 1x 15/50 rack
# 2x 96 pcr plate

tiprack_200ul = labware.load('tiprack-200ul', '10')
tiprack_10ul = labware.load('tiprack-10ul', '11')


tuberack_DNA = labware.load('tube-rack-2ml', '4')
tuberack_primers = labware.load('tube-rack-2ml', '6')
tuberack_mix = labware.load('tube-rack-2ml', '5')

# 15 ml tubes hold mastermix
# A1 and A2 have mastermix pre-made 
mm_tuberack = labware.load('tube-rack-15_50ml', '7')

# output plates
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
    s300.aspirate(200,tuberack_DNA.wells(i))
    for j in range(4):
        s300.dispense(50,output_plate_1.wells(8*(i)+j))
    s300.blow_out()
    s300.aspirate(200,tuberack_DNA.wells(i))
    for j in range(4,8):
        s300.dispense(50,output_plate_1.wells(8*(i)+j))
    s300.blow_out()
    s300.drop_tip()

    # s300.distribute(50, tuberack_mix.wells(i), output_plate_1.wells((8*(i)), to=((8*i)+(7)))) old way of doing it - but dripped


for i in range(12, 24):
    s300.pick_up_tip()
    s300.transfer(72, tuberack_DNA.wells(i), tuberack_mix.wells(i), mix_before=(3, 50), new_tip='never', mix_after=(5, 50))
    s300.aspirate(200,tuberack_DNA.wells(i))
    for j in range(4):
        s300.dispense(50,output_plate_2.wells(8*(i-12)+j))
    s300.blow_out()
    s300.aspirate(200,tuberack_DNA.wells(i))
    for j in range(4,8):
        s300.dispense(50,output_plate_2.wells(8*(i-12)+j))
    s300.blow_out()
    s300.drop_tip()

    # s300.distribute(50, tuberack_mix.wells(i), output_plate_2.wells((8*(i-12)), to=((8*(i-12))+7))) old way of doing it - but dripped









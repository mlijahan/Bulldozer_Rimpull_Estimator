import pandas as pd
import numpy as np
import math



class Machine:
    def __int__(self, model, power, weight, blade,speeds):
        self.Model = model
        self.Power = power
        self.Weight = weight
        self.Blade = blade


    def machine_name(self):
        manufacturer_case = manufacturer.upper()
        model_case = model_name.upper()
        blade_type_case = blade_type.upper()
        self.modelname = []
        return self.modelname.append(f'{manufacturer_case} {model_case} {blade_type_case}')


    def real_power(self):
        temp = (273+temperature) / 288.6
        root_temp = math.sqrt(temp)
        power_real = power / ((76/height_air_pressure()) * root_temp)
        self.reality_power = np.round(power_real, 2)
        return self.reality_power


    def rimpull_max(self, e=0.85):
        speeds = []
        ques = int(input("Enter number of gears of the dozer then velocities for per gear respectively: "))
        for i in range(0, ques):
            speed = float(input())
            speeds.append(speed)
        self.max_rimpull = (375 * self.reality_power * e) / (np.array(speeds)*0.278)
        print(self.max_rimpull)
        return(self.max_rimpull)

    def max_possible_rimpull(self):
        machine_weight_lb = machine_operation_weight() * 2000
        usable_force = machine_weight_lb * road
        self.possible_rimpull = []
        for x in self.max_rimpull:
            if usable_force < x:
                self.possible_rimpull.append(usable_force)
            else:
                self.possible_rimpull.append(x)
        print(self.possible_rimpull)
        return(np.round(self.possible_rimpull))


    def power_available(self):
        self.drawbar = np.array(self.possible_rimpull) - total_resistance()
        print(self.drawbar)
        return self.drawbar



def height_air_pressure():
    height_above_see_m = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000]
    airpress_cmhg = [76, 73.3, 70.66, 68.07, 65.58, 63.17, 60.83, 58.6, 56.41, 54.25, 52.2]
    y_new = np.interp(altitude, height_above_see_m, airpress_cmhg)
    return y_new


def read_excel():
    file = 'Bulldozer_data.xlsx'
    sheet = pd.ExcelFile(file)
    return sheet

def read_traction_cf():
    df = read_excel().parse('Traction Coefficient')
    Row_list = []
    for index, rows in df.iterrows():
        my_list = [rows.Rubber_Tiers_max, rows.Crawler_Tracks_max]
        Row_list.append(my_list)
    tc = []

    def rubber_tire():
        options_input_material = [*range(1, 8)]
        Rubber_Tiers_tcmax = [x[1] for x in Row_list]
        Rubber_Tiers_tcmax_dict = dict(zip(options_input_material, Rubber_Tiers_tcmax))
        for key, value in Rubber_Tiers_tcmax_dict.items():
            if key == surface:
                rollingresistance = value
                tc.append(rollingresistance)

        return tc

    def crawler():
        options_input_material = [*range(1, 8)]
        Crawler_tc_max = [x[1] for x in Row_list]
        Crawler_tc_max_dict = dict(zip(options_input_material, Crawler_tc_max))
        for key, value in Crawler_tc_max_dict.items():
            if key == surface:
                rollingresistance = value
                tc.append(rollingresistance)

        return tc

    def surfacetire_rubber():
        if track_tier == 2:
            return rubber_tire()
        else:
            return surfacetire_crawler()

    def surfacetire_crawler():
        if track_tier == 3:
            return crawler()

    surfacetire_rubber()
    return tc


def read_rimpullresistance():
    df = read_excel().parse('Rolling Resistance')
    Row_list = []
    for index, rows in df.iterrows():
        my_list = [rows.Surface_Type, rows.SteelTiers_Rrmax,
                   rows.Crawler_RRmax, rows.RubberTiers_HighPress_RRmax]
        Row_list.append(my_list)
    rr = []
    def steel_tire():
        options_input_material = [*range(1, 8)]
        Steel_Tiers_Rrmax = [x[1] for x in Row_list]
        Steel_Tiers_Rrmax_dict = dict(zip(options_input_material, Steel_Tiers_Rrmax))
        for key, value in Steel_Tiers_Rrmax_dict.items():
            if key == surface:
                rollingresistance = value
                rr.append(rollingresistance)
        return rr

    def rubber_tire():
        options_input_material = [*range(1, 8)]
        Rubber_Tiers_HighPress_RRmax = [x[3] for x in Row_list]
        Rubber_Tiers_HighPress_RRmax_dict = dict(zip(options_input_material, Rubber_Tiers_HighPress_RRmax))
        for key, value in Rubber_Tiers_HighPress_RRmax_dict.items():
            if key == surface:
                rollingresistance = value
                rr.append(rollingresistance)

        return rr

    def crawler():
        options_input_material = [*range(1, 8)]
        Crawler_RR_max = [x[2] for x in Row_list]
        Crawler_RR_max_dict = dict(zip(options_input_material, Crawler_RR_max))
        for key, value in Crawler_RR_max_dict.items():
            if key == surface:
                rollingresistance = value
                rr.append(rollingresistance)

        return rr

    def surfacetire_steel():
        if track_tier == 1:
            return steel_tire()
        else:
            return surfacetire_rubber()

    def surfacetire_rubber():
        if track_tier == 2:
            return rubber_tire()
        else:
            return surfacetire_crawler()

    def surfacetire_crawler():
        if track_tier == 3:
            return crawler()

    surfacetire_steel()
    return rr


def machine_operation_weight():
    material_in_blade_tn= (blade * read_material()*0.001) + gross_weight_ton(weight)
    return material_in_blade_tn

def gross_weight_ton(weight):
    return 0.001 * weight

def total_resistance():
    equivalent_grade = (np.array(read_rimpullresistance()) / 20) + slop
    grade_overcome_resistance = machine_operation_weight()*(20*equivalent_grade)
    force_overcome_rollingresistance = machine_operation_weight()* (np.array(read_rimpullresistance()))
    whole_resistance = grade_overcome_resistance + force_overcome_rollingresistance
    print(whole_resistance)
    return whole_resistance


class Site():
    def __int__(self, surface, slop, temperature, altitude, road):
        self.Surface = surface
        self.Slop = slop
        self.Temperature = temperature
        self.Altitude = altitude
        self.Road = road


def read_material():
    df = read_excel().parse('Material')
    Row_list = []
    for index, rows in df.iterrows():
        my_list = [rows.Material_Type, rows.Loose_weight_Kgm3, rows.Bank_weight_Kgm3, rows.Load_Factors]
        Row_list.append(my_list)
    options_input_material = [*range(1, 23)]
    loose_weight_material = [x[1] for x in Row_list]
    loose_weight_material_dict = dict(zip(options_input_material, loose_weight_material))
    for key, value in loose_weight_material_dict.items():
        if key == material:
            density = value
            return density


class Activity ():
    def __int__(self, name, material):
        self.Name = name
        self.Material = material



manufacturer = input("Insert the manufacturer name of the bulldozer:\n\n")
model_name = input("Insert the model name of the bulldozer:\n\n")
blade_type = input("Insert blade type name of the bulldozer:\n\n")
power = int(input("Insert the power of the bulldozer (hp):\n\n"))
weight = int(input("Insert the operation weight of the bulldozer (kg):\n\n"))
blade = int(input("Insert the capacity of the bulldozer blade (m3):\n\n"))
surface = int(input("Choose the surface of the road: \n(1) Smooth concrete"
                        "\n(2) Good asphalt\n(3) Earth, compacted and maintained\n"
                    "(4) Earth, compacted and maintained\n(5) Earth, rutted, muddy, no maintenance\n"
                    "(6) Loose sand and grave\n(7) Earth, very muddy, rutted, soft\n\n"))
track_tier = int(input("Enter type of the track or tire of bulldozer: \n(1) steel tire "
                                "\n(2)rubber tire \n(3)crawler \n\n"))
road = int(input("Choose the surface type of the road considering traction of material: \n(1) Dry, rough concrete"
                        "\n(2) Dry, clay loam\n(3) Wet, clay loam\n(4) Wet sand and gravel\n(5) Loose, dry sand\n(6) Dry snow"
                 "\n(7)Ice \n\n"))
slop = int(input("please insert percent of slop:\n\n"))
temperature = int(input("Insert the mean of the temperature in duration of doing activity (C) :\n\n"))
altitude = int(input("Insert the mean of the elevation of the job site (m) :\n\n"))
activity = input("Insert the title of the activity:\n\n")
material = int(input("Choose the material that is going to be hauling: \n(1) 'Ash, Bituminous Coal'"
                         "\n(2) 'Basalt'\n(3) 'Bauxite, Kaolin\n(4) 'Bituminous, Raw'\n\n"))



def main():
    d= Machine()
    d.machine_name()
    d.real_power()
    d.rimpull_max()
    d.max_possible_rimpull()
    read_rimpullresistance()
    read_material()
    read_traction_cf()
    d.power_available()





if __name__ == "__main__":
    main()


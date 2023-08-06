# -*- coding: utf-8 -*-

""" Estimation of available rimpull of track/tire bulldozer during hauling material """

import pandas as pd
import numpy as np
import math
import datetime
import matplotlib.pyplot as plt


class Site:
    """ Atributes of job site are defined in this class"""
    def __int__(self, surface, slop, temperature, altitude, road, name, material):
        self.Surface_rolling_resistance = surface  # Rolling Resistance of hauling roade's surface
        self.Slop = slop  # Natural Grade of hauling road
        self.Temperature = temperature  # Mean of Natural Temperature of job site during doing the activity
        self.Altitude = altitude   # Mean of height of job site above the sea
        self.Road = road   # Road's surface material
        self.Name = name   # Title of Activity
        self.Material = material   # Type of hauling material


    def material_type(self,material):
        """ Define the density of loosing material (kg/m3) using the Excel file. The file is prepared
        based on *** """
        df = read_excel().parse('Material')
        Row_list = []
        for index, rows in df.iterrows():
            my_list = [rows.Material_Type, rows.Loose_weight_Kgm3, rows.Bank_weight_Kgm3, rows.Load_Factors]
            Row_list.append(my_list)
        options_input_material = [*range(1, 50)]
        loose_weight_material = [x[1] for x in Row_list]
        loose_weight_material_dict = dict(zip(options_input_material, loose_weight_material))
        for key, value in loose_weight_material_dict.items():
            if key == material:
                self.Material = value
                return self.Material

    def rolling_resistance_road(self, surface):
        """ Define amount of rolling resistandce (lb/ton) for various road surfaces considering surface material
         and type of track or wheel, using the Excel file. The file reference is :
          *** """
        df = read_excel().parse('Rolling Resistance')
        Row_list = []
        for index, rows in df.iterrows():
            my_list = [rows.Surface_Type, rows.SteelTiers_Rrmax,
                       rows.Crawler_RRmax, rows.RubberTiers_HighPress_RRmax]
            Row_list.append(my_list)
        rr = []
        self.Surface_rolling_resistance = rr

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

    def traction_cf_road(self, road):
        """ Define amount of traction coefficient for various road surfaces considering surface material
         and type of track or wheel, using the Excel file. The file reference is :
          *** """
        df = read_excel().parse('Traction Coefficient')
        Row_list = []
        for index, rows in df.iterrows():
            my_list = [rows.Rubber_Tiers_max, rows.Crawler_Tracks_max]
            Row_list.append(my_list)
        tc = []
        self.Road = tc

        def rubber_tire():
            options_input_material = [*range(1, 8)]
            Rubber_Tiers_tcmax = [x[1] for x in Row_list]
            Rubber_Tiers_tcmax_dict = dict(zip(options_input_material, Rubber_Tiers_tcmax))
            for key, value in Rubber_Tiers_tcmax_dict.items():
                if key == road:
                    rollingresistance = value
                    tc.append(rollingresistance)
            return tc

        def crawler():
            options_input_material = [*range(1, 8)]
            Crawler_tc_max = [x[1] for x in Row_list]
            Crawler_tc_max_dict = dict(zip(options_input_material, Crawler_tc_max))
            for key, value in Crawler_tc_max_dict.items():
                if key == road:
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

    def equivalent_grade(self,slop):
        """ Define equivalent gradient of haulin road as bottom equation :
            Rolling resistance expressed in #lb/U.S. ton# / 20 #lb/U.S. ton# = G%"""
        eq_grade = (np.array(self.Surface_rolling_resistance)) / 20
        self.Slop = eq_grade + slop
        return self.Slop

    def height_air_pressure(self, altitude):
        """ Define the air pressure (CmhG) of job site in dependence of the height (m) of site above the see """
        height_above_see_m = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000]     # possible heights of jobsites
        airpress_cmhg = [76, 73.3, 70.66, 68.07, 65.58, 63.17, 60.83, 58.6, 56.41, 54.25, 52.2]
        self.y_new = np.interp(altitude, height_above_see_m, airpress_cmhg)
        return self.y_new

    def site_temprature_effect(self, temperature):
        """ Define the Temperature of job site in K """
        temp = (273 + temperature) / 288.6    # convert temperature in Celsius to Kelvin
        self.Temperature = math.sqrt(temp)
        self.Temperature
        return self.Temperature


class Machine(Site):
    """ Atributes of bulldozers and rimpull resistance and gradient resistance of
     dozers during per hauling activity are defined in this class"""
    def __int__(self, power, weight, blade,speeds, **kwargs):
        super(Machine, self).__init__(**kwargs)
        self.Power = power      # Rated power SAE (net)
        self.Weight = weight    # Operating Weight of Machine
        self.Blade = blade      # Blade Capacity


    def machine_name(self, manufacturer, model_name, blade_type):
        """ Define the fullname of machine as:
        Mnufacturer's name + Tractor's model name + type of blade of bulldozer (S( Straight blade), U( Universal blade), SU(Semi U),...)"""
        manufacturer_case = manufacturer.upper()
        model_case = model_name.upper()
        blade_type_case = blade_type.upper()
        self.machinename = f'{manufacturer_case} {model_case} {blade_type_case}'


    def machine_operation_weight(self,weight):
        """ Define Machine's weight as:
        Operating Weight (with full fuel tank and operator) + blade's wight + matrial's weight inside blade"""
        super().material_type(material)
        gross_weight_ton = 0.001 * weight
        self.material_in_blade_tn = (blade * self.Material * 0.001) + gross_weight_ton
        return  self.material_in_blade_tn


    @property
    def real_power(self):
        """ Real Horsepower Rating in job site condition (Elevation&Temperature of job site make changes in Rated power SAE"""
        super().height_air_pressure(altitude)
        super().site_temprature_effect(temperature)
        power_real = power / ((76/self.y_new) * self.Temperature)
        self.reality_power = np.round(power_real, 2)
        return self.reality_power

    def rimpull_max(self, e=0.85):
        """  Define the maximum rimpull as a function of the power of the
            engine and the gear ratio between the engine and the driving wheels. The following equation
            can be used to determine maximum rimpull:
            RP (375 * HP * e)/V
            maximum rimpull changes in each gear (different velocity) """
        self.speeds = []
        ques = int(input("Enter number of gears of the dozer then maximum velocities for per gear respectively: "))
        for i in range(0, ques):
            speed = float(input())
            self.speeds.append(speed)
        self.max_rimpull = (375 * self.reality_power * e) / (np.array(self.speeds)*0.278)
        return(self.max_rimpull)

    @property
    def max_possible_rimpull(self):
        """ The power to do work is often limited by traction. The factors controlling
            usable horsepower are the weight on the powered running gear, the characteristics of
            the running gear, and the characteristics of the travel surface:
            Usable force = Coefficient of traction × Weight on powered running gear """
        machine_weight_lb = self.material_in_blade_tn * 2000  # Converting machine's wweight from (ton) to (lb)
        usable_force = machine_weight_lb * road
        self.possible_rimpull = []
        for x in self.max_rimpull:
            if usable_force < x:
                self.possible_rimpull.append(usable_force)
            else:
                self.possible_rimpull.append(x)
        return self.possible_rimpull

    @property
    def total_resistance(self):
        """ Define the force required to overcome grade resistance and
        force required to overcome rolling resistance"""
        super().rolling_resistance_road(surface)
        super().equivalent_grade(slop)
        self.force_overcome_rollingresistance = self.material_in_blade_tn * np.array(self.Surface_rolling_resistance)
        self.force_overcome_graderesistance = self.material_in_blade_tn*(20*self.Slop)
        self.whole_resistance = self.force_overcome_graderesistance + self.force_overcome_rollingresistance
        return self.whole_resistance

    @property
    def power_available(self):
        """ Power available for towing a load """
        self.drawbar = np.array(self.possible_rimpull) - self.whole_resistance
        self.drawbar_list = list(self.drawbar)
        return self.drawbar

    @property
    def rimpull_allowable(self):
        """ If drawpull of the bulldozer in each gear is greater than whol total resistance, then bulldozer is
        alowable to haul material on that particular gear on the hauling road. """
        for x in self.drawbar_list:
            if x > self.whole_resistance:
                print(
                    f'"{self.machinename}" is allowable for doing "{activity}" in max velocity of gear number {self.drawbar_list.index(x)+1} with rimpull "{np.round(x)} lb"')
            else:
                print(
                    f'"{self.machinename}" is not allowable for doing "{activity}" in max velocity of gear number {self.drawbar_list.index(x)+1} with rimpull "{np.round(x)} lb"')


    @property
    def rimpull_available_velocity_graph(self):
        """ illusterate varing drawbarpull with changin velocities for varipus gears. """
        Geb_a30 = [17915.08453237, 5258.2307297, 1302.96391637]
        years_a30 = [5, 10.5, 16]
        fig, ax = plt.subplots()
        ax.plot(self.speeds, self.drawbar_list, label=' Rimpull', color='red')
        legend = ax.legend(loc='center right', fontsize='x-large')
        plt.xlabel('V (Km/hr)')
        plt.ylabel('Rimpull (lb)')
        plt.title('Available Rimpull for maximum velosities of gears')
        plt.show()
        plt.close()


def read_excel():
    file = 'Bulldozer_data.xlsx'
    sheet = pd.ExcelFile(file)
    return sheet


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
material = int(input("Choose the material that is going to be hauling: \n(1) Ash, Bituminous Coal"
                             "\n(2) Basalt\n(3) Bauxite, Kaolin\n(4) Bituminous, Raw\n(5) Bituminous, washed\n"
                     "(6) Caliche\n\n"))


def main():
    bulldozer = Machine()
    bulldozer.machine_name(manufacturer, model_name, blade_type)
    bulldozer.machine_operation_weight(weight)
    bulldozer.real_power
    bulldozer.rimpull_max()
    bulldozer.total_resistance
    bulldozer.max_possible_rimpull
    bulldozer.power_available
    bulldozer.rimpull_allowable
    bulldozer.rimpull_available_velocity_graph




if __name__ == "__main__":
    main()


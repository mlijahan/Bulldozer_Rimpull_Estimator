

class Machine:
    def __int__(self, model, power, weight, blade):
        self.Model = model
        self.Power = power
        self.Weight = weight
        self.Blade = blade

    def machine_name(self):
        manufacturer_case = manufacturer.upper()
        model_case = model_name.upper()
        blade_type_case = blade_type.upper()
        return f'{manufacturer_case} {model_case} {blade_type_case}'


    def machine_operation_weight(self):
        operation_weight = weight + blade



class Site:
    def __int__(self, surface, slop, temperature, altitude):
        self.Surface = surface
        self.Slop = slop
        self.Temperature = temperature
        self.Altitude = altitude


class Activity:
    def __int__(self, name, material, wheel_sleep):
        self.Name = name
        self.Material = material
        self.Wheel_Sleep = wheel_sleep

    def material_weight(self):
        self.density = 14

    def blade_add_material(self):
        material_weight = blade * self.density
        blade_add_to_material = blade * self.density


manufacturer = input("Insert the manufacturer name of the bulldozer:\n\n")
model_name = input("Insert the model name of the bulldozer:\n\n")
blade_type = input("Insert blade type name of the bulldozer:\n\n")
power = int(input("Insert the power of the bulldozer (hp):\n\n"))
weight = int(input("Insert the operation weight of the bulldozer (kg):\n\n"))
blade = int(input("Insert the capacity of the bulldozer blade (m3):\n\n"))
# surface = int(input("Choose the surface of the road: \n(1) 'Ash, Bituminous Coal'"
#                         "\n(2) 'Basalt'\n(3) 'Bauxite, Kaolin\n(4) 'Bituminous, Raw'\n\n")
#                   )
# slop = int(input("please insert percent of slop:\n\n"))
# temperature = int(input("Insert the mean of the temperature in duration of doing activity (m) :\n\n"))
# altitude = int(input("Insert the mean of the elevation of the job site (m) :\n\n"))
# activity = input("Insert the title of the activity:\n\n")
# material = int(input("Choose the material that is going to be hauling: \n(1) 'Ash, Bituminous Coal'"
#                          "\n(2) 'Basalt'\n(3) 'Bauxite, Kaolin\n(4) 'Bituminous, Raw'\n\n")
#                    )
# wheel_sleep = int(input("please insert wheel sleep mm:\n\n"))

def main():
    machine_call = Machine()
    model = machine_call.machine_name()
    print(model)



if __name__ == "__main__":
    main()


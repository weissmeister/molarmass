# All known atoms with their atomic masses, used for calculations. Some atoms do not appear in nature but who cares.
atoms = {"H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.811, "C": 12.011, "N": 14.007, "O": 15.999,
         "F": 18.998, "Ne": 20.18, "Na": 22.99, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974, "S": 32.065,
         "Cl": 35.453, "Ar": 39.948, "K": 39.098, "Ca": 40.078, "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996,
         "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.39, "Ga": 69.723, "Ge": 72.64,
         "As": 74.922, "Se": 78.96, "Br": 79.904, "Kr": 83.8, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
         "Nb": 92.906, "Mo": 95.94, "Tc": 98, "Ru": 101.07, "Rh": 102.906, "Pd": 106.42, "Ag": 107.868, "Cd": 112.411,
         "In": 114.818, "Sn": 118.71, "Sb": 121.76, "Te": 127.6, "I": 126.905, "Xe": 131.293, "Cs": 132.906,
         "Ba": 137.327, "La": 138.906, "Ce": 140.116, "Pr": 140.908, "Nd": 144.24, "Pm": 145, "Sm": 150.36,
         "Eu": 151.964, "Gd": 157.25, "Tb": 158.925, "Dy": 162.5, "Ho": 164.93, "Er": 167.259, "Tm": 168.934,
         "Yb": 173.04, "Lu": 174.967, "Hf": 178.49, "Ta": 180.948, "W": 183.84, "Re": 186.207, "Os": 190.23,
         "Ir": 192.217, "Pt": 195.078, "Au": 196.967, "Hg": 200.59, "Tl": 204.383, "Pb": 207.2, "Bi": 208.98,
         "Po": 209, "At": 210, "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232.038, "Pa": 231.036, "U": 238.029,
         "Np": 237, "Pu": 244, "Am": 243, "Cm": 247, "Bk": 247, "Cf": 251, "Es": 252, "Fm": 257, "Md": 258, "No": 259,
         "Lr": 262, "Rf": 261, "Db": 262, "Sg": 266, "Bh": 264, "Hs": 277, "Mt": 268}


def calcmolmass(inputstr):  # Function  to calcumate the molar mass
    # Returns success (bool), molar mass (float, 0.0 on no success) and error message (str, empty on success)
    totalmass = 0.0
    element = ""
    amount = ""
    bracketamount = ""
    molecule = {}
    withinbrackets = {}
    bracketstate = 0  # 0 = before brackets, 1 = within brackets, 2 = right after brackets

    for char in inputstr:

        if char == "(":  # Beginning of a bracketed part
            if bracketstate == 1:
                return False, 0.0, "Nested brackets are not supported"

            bracketstate = 1

            if len(element) != 0:  # If the length of the element is 0, the bracket is at the beginning of the molecule
                if len(amount) == 0:
                    amount = 1
                else:
                    amount = int(amount)

                if element not in atoms:
                    return False, 0.0, "{0} is not a valid element abbreviation.".format(element)

                molecule[element] = molecule.get(element, 0) + amount
                amount = ""
                element = ""

        elif char == ")":
            bracketstate = 2

        elif char.isalpha():
            if char.isupper() and len(element) == 0:  # First element
                element = char

            elif char.islower() and len(element) == 1:
                element = element + char

            elif char.islower() and len(element) > 1:
                return False, 0.0, "Element abbreviations can only be one or two letters," \
                                   " the first upper- and the second lowercase."

            elif char.isupper() and len(element) != 0: # new element is being specified, add previous one to the dict
                if element not in atoms:
                    return False, 0.0, "{0} is not a valid element abbreviation.".format(element)

                if len(amount) == 0:
                    amount = 1
                else:
                    amount = int(amount)

                if bracketstate == 0:  # Normal situation, specified element is not in brackets
                    molecule[element] = molecule.get(element, 0) + amount
                    amount = ""
                    element = char

                elif bracketstate == 1:  # Element is within the brackets
                    withinbrackets[element] = withinbrackets.get(element, 0) + amount
                    amount = ""
                    element = char

                elif bracketstate == 2:  # Element is just outside brackets, need to process stuff within the brackets
                    withinbrackets[element] = withinbrackets.get(element, 0) + amount
                    amount = ""
                    element = char

                    if len(bracketamount) == 0:
                        bracketamount = 1
                    else:
                        bracketamount = int(bracketamount)

                    for element2 in withinbrackets:  # Add the atoms in within the brackets to the main molecule
                        withinbrackets[element2] = withinbrackets[element2] * bracketamount
                        molecule[element2] = molecule.get(element2, 0) + withinbrackets[element2]

                    bracketstate = 0  # Clear variables
                    bracketamount = ""
                    withinbrackets = {}

            elif char.islower() and len(element) == 0:
                return False, 0.0, "Element abbreviations always start with an uppercase letter, not lowercase."

        elif char.isdigit():
            if bracketstate != 2:
                if len(element) == 0:
                    return False, 0.0, "You have specified a digit before specifying an element."
                amount = amount + char

            elif bracketstate == 2:
                bracketamount = bracketamount + char

        else:  # Not a bracket, letter or digit
            return False, 0.0, "Invalid sign ({0}). You can only put in letters, " \
                               "digits and brackets.".format(char)

    # Code to process last element
    if element not in atoms:
        return False, 0.0, "{0} is not a valid element abbreviation.".format(element)

    if len(amount) == 0:
        amount = 1
    else:
        amount = int(amount)

    if bracketstate == 0:
        molecule[element] = molecule.get(element, 0) + amount

    elif bracketstate == 1:
        return False, 0.0, "Your brackets are not closed."

    elif bracketstate == 2:
        withinbrackets[element] = withinbrackets.get(element, 0) + amount

        if len(bracketamount) == 0:
            bracketamount = 1
        else:
            bracketamount = int(bracketamount)

        for element in withinbrackets:  # Add the atoms in within the brackets to the main molecule
            withinbrackets[element] = withinbrackets[element] * bracketamount
            molecule[element] = molecule.get(element, 0) + withinbrackets[element]

    # Add up the masses
    for atom in molecule:
        count = molecule[atom]
        mass = atoms[atom]
        totalmass += count * mass

    return True, round(totalmass, 3), ""

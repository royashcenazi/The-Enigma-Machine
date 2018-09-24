import copy


class Rotor:

    def __init__(self, rentries, lentries, lrotor, notch):
        self.rentries = rentries
        self.lentries = lentries
        self.lrotor = lrotor
        self.notch = notch

    def rotate(self):
            self.lentries = self.lentries[-1:] + self.lentries[:-1]
            self.rentries = self.rentries[-1:] + self.rentries[:-1]
            self.notch -= 1
            if self.notch == 0 and self.lrotor is not None:
                self.lrotor.rotate()

            if self.notch == -1:
                self.notch = len(self.lentries)

    def get_from_right(self, ind):
        return self.__go_throw_rotors(self.rentries, self.lentries, ind)

    def get_from_left(self, ind):
        return self.__go_throw_rotors(self.lentries, self.rentries, ind)

    def __go_throw_rotors(self, in_entreis, out_entries, ind):
        find = in_entreis[ind - 1]
        entrance = 1
        for x in out_entries:
            if x == find:
                return entrance
            entrance += 1


class Reflector:

    def __init__(self, reflections):
        self.reflections = reflections

    def get_reflection(self, num):
        for (left, right) in self.reflections:
            if num == left: return right
            if num == right: return left


class Machine:

    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def decrypt_string(self, encrypt):
        res = []
        numbers = self.__string_to_numbers(encrypt)
        for fig in numbers:
            res.append(self.__decrypt_letter(fig))

        return self.__numbers_to_string(res)

    def __decrypt_letter(self, letter):
        res = letter
        for i in reversed(range(len(self.rotors))):
            if i == (len(self.rotors) - 1): self.rotors[i].rotate()
            res = self.rotors[i].get_from_right(res)

        res = self.reflector.get_reflection(res)

        for rotor in self.rotors:
            res = rotor.get_from_left(res)

        return res

    def __string_to_numbers(self, to_encrypt):
        res = [ord(char) - 96 for char in to_encrypt.lower()]
        return res

    def __numbers_to_string(self, encrypted):
        res = [chr(x + 96) for x in encrypted]
        return res


def main():
    refl = Reflector([(1, 4), (2, 5), (3, 6)])
    rotor1 = Rotor([1, 2, 3, 4, 5, 6], [5, 2, 4, 6, 3, 1], None,  4)
    rotor2 = Rotor([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], rotor1, 1)
    machine = Machine([rotor1, rotor2], refl)
    machine2 = copy.deepcopy(machine)
    print(machine.decrypt_string("aabbcc"))
    print(machine2.decrypt_string("dbecfd"))



if __name__ == '__main__':
    main()




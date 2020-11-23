class Count:

    def __init__(self, name):
        self.name = name
        self.count = 0

    def get_name(self):
        return self.name
    def set_count(self):
        self.count = self.count + 1

    def get_count(self):
        return self.count

class Species(Count):
    def __init__(self, name):
        super().__init__(name)
        self.restriction_sites = []
        self.profile = []
        self.profile_joined = None

    def set_restriction(self, enzyme):
        self.restriction_sites.append(enzyme)

    def get_restriction(self):
        return self.restriction_sites

    def set_profile(self, result):
        if result == True:
            self.profile.append(str(1))
        elif result == False:
            self.profile.append(str(0))

    def get_profile(self):
        self.profile_joined = ''.join(self.profile)
        return self.profile_joined

    def reset_profile(self):
        self.profile = []
        self.profile_joined = None

class Enzyme(Count):
    def __init__(self, name):
        super().__init__(name)
        self.points = 0
        self.total = 0

    def set_points(self, new_value):
        old_total = self.points * self.total
        self.total = self.total + 1
        new_total = (old_total + new_value) / self.total
        self.points = round(new_total, 3)

    def get_points(self):
        return self.points

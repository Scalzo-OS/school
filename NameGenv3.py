import string


class NameGen:
    def __init__(self):
        # defining variables, m/male, f/female
        self.name_m = []
        self.number_m = []
        self.f_let_m = {}
        self.name_f = []
        self.number_f = []
        self.f_let_f = {}
        self.tot_f = 839
        self.tot_m = 1794

    def write_data(self, sex):
        import string
        import csv
        x = list(string.ascii_lowercase + string.punctuation)
        with open('name_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for i in x:
                writer.writerow([f'_{i}_{sex}_'])
                for item, value in self.__dict__[f'{i}_follow_{sex}'].items():
                    writer.writerow([item, value])

    def read_data(self):
        import csv
        import string
        try:
            open('name_data.csv', 'x')
            self.write_data('f')
            self.write_data('m')
        except FileExistsError:
            self.read_sc()

        i = 0
        tot_i = 58
        x = list(string.ascii_lowercase + string.punctuation)
        with open('name_data.csv', 'r') as f:
            reader = csv.reader(f)
            while i < tot_i:
                for i in x:
                    i += 1

    def read_sc(self):
        import csv
        import string
        with open('babies-first-names-all-names-all-years.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if 'B' in row[1]:  # add male name and no
                    self.name_m.append(row[2])
                    self.number_m.append(int(row[3]))
                if 'G' in row[1]:
                    self.name_f.append(row[2])
                    self.number_f.append(int(row[3]))

        x = list(string.ascii_lowercase + string.punctuation)
        y = list(string.ascii_uppercase)

        for idx, item in enumerate(x):
            self.__dict__[f'{item}_follow_m'] = {}  # create dict for pairs
            self.__dict__[f'{item}_follow_f'] = {}
            for i in x:
                self.__dict__[f'{item}_follow_m'][i] = 0  # default value is 0 for all char
                self.__dict__[f'{i}{item}_follow_m'] = {}  # create dict for groups of 3
                self.__dict__[f'{item}{i}_follow_m'] = {}
                self.__dict__[f'{item}_follow_f'][i] = 0  # default value is 0 for all char
                self.__dict__[f'{i}{item}_follow_f'] = {}  # create dict for groups of 3
                self.__dict__[f'{item}{i}_follow_f'] = {}
                for z in x:
                    self.__dict__[f'{i}{item}_follow_f'][z] = 0
                    self.__dict__[f'{item}{i}_follow_f'][z] = 0
                    self.__dict__[f'{i}{item}_follow_m'][z] = 0
                    self.__dict__[f'{item}{i}_follow_m'][z] = 0
        for i in y:
            self.f_let_m[i] = 0
            self.f_let_f[i] = 0

    def weigh_follow(self, word, number, sex):
        word = list(word.lower())
        for idx, item in enumerate(word):
            if len(word) > idx + 1:
                self.__dict__[f'{item}_follow_{sex}'][word[idx + 1]] += number / self.__dict__[f'tot_{sex}']
            if len(word) > idx + 2:
                self.__dict__[f'{item}{word[idx + 1]}_follow_{sex}'][word[idx + 2]] += number / self.__dict__[
                    f'tot_{sex}']

    def collect_weights(self):
        for i in range(len(self.name_f)):
            self.weigh_follow(self.name_f[i], self.number_f[i], 'f')
            self.f_let_f[self.name_f[i][0]] += self.number_f[i] / self.tot_f
        for i in range(len(self.name_m)):
            self.weigh_follow(self.name_m[i], self.number_m[i], 'm')
            self.f_let_m[self.name_m[i][0]] += self.number_m[i] / self.tot_m

    def gen_name(self, sex, length):
        import random
        f_let_list = [i.lower() for i in self.__dict__[f'f_let_{sex}']]
        f_let_weights = [self.__dict__[f'f_let_{sex}'][i] for i in self.__dict__[f'f_let_{sex}']]
        n = list(random.choices(f_let_list, weights=f_let_weights)[0])
        for i in range(length):
            if len(n) > 1 and '~' not in n:
                curr_let = ''.join([n[i], n[i-1]])
            else:
                curr_let = ''.join(n[i]).replace('~', 'a')
            curr_let_r = [i for i in self.__dict__[f'{curr_let}_follow_{sex}']]
            curr_let_w = [self.__dict__[f'{curr_let}_follow_{sex}'][i] for i in
                          self.__dict__[f'{curr_let}_follow_{sex}']]
            n.append(random.choices(curr_let_r, weights=curr_let_w)[0])
        n[0] = n[0].upper()
        n = ''.join(n)
        return n

    def return_dict(self, follow, letter, sex):
        return self.__dict__[f'{follow}_follow_{sex}'][letter]

    def update_dict(self, follow, letter, sex, value):
        self.__dict__[f'{follow}_follow_{sex}'][letter] = value
        print(f'{follow}_follow_{sex} updated {letter} to {value}')

name = NameGen()
name.read_sc()
name.collect_weights()

while True:
    print(name.gen_name('m', 5))
    input()

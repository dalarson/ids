from faker import Faker

fake = Faker()
for _ in range(1000):
    name = fake.name()
    ssn = fake.ssn()
    print("{}\t{}".format(name, ssn))

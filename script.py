from app import *
from datetime import datetime

print ("deleting old database" )
db.drop_all()
print ("creating new database" )
db.create_all()


# # ============================== Section ===============================
print ("Entering the data in section table\n")
print("....................................\n")

f= open('section_data.csv','r')
header = f.readline().strip()  # Read and ignore the header line
for data in f.readlines():
    data = data.strip()
    last_comma_index = data.rfind(',')
    name = data[:last_comma_index].strip()
    image_url = data[last_comma_index + 1:].strip()
    section = Section(name = name,image_url=image_url)
    db.session.add(section)
f.close()


print("commiting the database")
print("....................................\n")
# db.session.add_all([t1,t2,t3,t4,t5,t6,t7,t8,t9])
try:
    db.session.commit()
    print("data successfully entered into section table\n\n")
except Exception as e:
    print("data can not be added to section table",e)

# # ============================== Products ===============================
print("....................................\n")

with open('products_data.csv', 'r') as f:
    header = f.readline().strip()  # Read and ignore the header line

    for line in f.readlines():
        line = line.strip().split(',')

        if len(line) != 8:
            print(f"Invalid data format for line: {','.join(line)}")
            continue

        try:
            product = Product(
                name=line[0],
                brand=line[1],
                manufacturing_date=datetime.strptime(line[2], '%d/%m/%Y').date(),
                expiry_date=datetime.strptime(line[3], '%d/%m/%Y').date(),
                price=float(line[4]),
                stock=int(line[5]),
                # image_url=line[6],
                section_id=int(line[7])
            )
            db.session.add(product)
        except (ValueError, IndexError) as e:
            print(f"Error processing line: {','.join(line)} - {e}")
            continue


print("commiting the database")
print("....................................\n")
# db.session.add_all([t1,t2,t3,t4,t5,t6,t7,t8,t9])
try:
    db.session.commit()
    print("data successfully entered into product table\n\n")
except Exception as e:
    print("data can not be added to product table",e)

# ============================== User ===============================
print ("Entering th..................into USER.\n")


with open('user_data.csv', 'r') as f:
    header = f.readline().strip()  # Read and ignore the header line

    for line in f.readlines():
        line = line.strip().split(',')

        if len(line) != 9:
            print(f"Invalid data format for line: {','.join(line)}")
            continue

        try:
            product = User(
                name=line[0],
                username=line[1],
                password=hash_password(line[2]),
                email=line[3],
                mobile=int(line[4]),
                address=line[5],
                city=line[6],
                state=line[7],
                pin=int(line[8])
            )
            db.session.add(product)
        except (ValueError, IndexError) as e:
            print(f"Error processing line: {','.join(line)} - {e}")
            continue




print("commiting the database after USER")
print("....................................\n")
# db.session.add_all([t1,t2,t3,t4,t5,t6,t7,t8,t9])
try:
    db.session.commit()
    print("data successfully entered into USEr table\n\n")
except Exception as e:
    print("data can not be added to user table",e)

# # # ============================== Admin ===============================
# print ("Entering the data in Admin table\n")
# print("....................................\n")
# t1 = Admin(name="Shahid",username='admin1',password="admin",email="admin@aaa.com")
# t2 = Admin(name="Amir",username='admin2',password="admin",email="admin2@aaa.com")


# print("commiting the database")
# print("....................................\n")
# db.session.add_all([t1,t2])
# db.session.commit()
# print("data successfully entered into admin table\n\n")




import csv
with open('/media/LCA_PLC/USB DISK/parameters.csv', mode = 'r') as file:
    data = csv.reader(file)
    next(data, None)
    params = [row for row in data]
    print(params)

pos = [row[0] for row in params]
vel = [row[1] for row in params]
center = params[0][2]

print('positions: ', pos)
print('velocities: ', vel)
print('center: ', center)
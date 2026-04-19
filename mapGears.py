import math
import csv

teamNum = "42"
mapNum = input("Enter map number: ")
unitLen = float(input("Enter unit length: ")) 
unit = input("Enter unit type: ")

gridSize = 6 #Edit depending on grid size
start1 = int(input("Enter starting x grid coordinate: "))
start2 = int(input("Enter starting y grid coordinate: "))
gridOrigin = (start1, start2)

magThreshold = float(input("Enter magnetic threshold: "))
heatThreshold = float(input("Enter heat threshold: "))

grid = [[0 for i in range(gridSize)] for j in range(gridSize)]

startRow = (gridSize - 1) - start2
startCol = start1
grid[startRow][startCol] = 5

hazardsList = []

posX = start1 * unitLen
posY = start2 * unitLen

def processData(distanceMoved, imuYaw, irValue, magValue, isExit):
    global posX, posY

    driveRad = math.radians(imuYaw)
    posX += distanceMoved * math.cos(driveRad)
    posY += distanceMoved * math.sin(driveRad) 

    gridX = int(posX / unitLen)
    gridY = int(posY / unitLen)

    if 0 <= gridX < gridSize and 0 <= gridY < gridSize:
        row = (gridSize - 1) - gridY
        col = gridX

        if grid[row][col] not in [4, 5]:
            if isExit:
                grid[row][col] = 4
            elif magValue > magThreshold:
                grid[row][col] = 3
                logHazard("Magnetic Source", "Field Strength (uT)", magValue, posX, posY)
            elif irValue > heatThreshold:
                grid[row][col] = 2
                logHazard("Heat Source", "Radiated Power (W)", irValue, posX, posY)
            else:
                grid[row][col] = 1

def logHazard(hazType, parameter, value, x, y):
    hazardsList.append([hazType, parameter, value, round(x, 2), round(y, 2)])

def exportFiles():
    mapFileName = f"team{teamNum}_map.csv"
    with open(mapFileName, "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow([f"Team: {teamNum}"])
        writer.writerow([f"Map: {mapNum}"])
        writer.writerow([f"Unit Length: {unitLen}"])
        writer.writerow([f"Unit: {unit}"])
        writer.writerow([f"Origin: ({start1}, {start2})"])
        writer.writerow(["Notes: Autonomous Mapping of Disaster Zone"]) 
        for row in grid:
            writer.writerow(row)

    hazardsFileName = f"team{teamNum}_hazards.csv"
    with open(hazardsFileName, "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow([f"Team: {teamNum}"])
        writer.writerow([f"Map: {mapNum}"])
        writer.writerow(["Notes: Hazard Detection Log"]) 
        writer.writerow([])
        writer.writerow(["Hazard Type", "Parameter of Interest", "Parameter Value", f"Hazard X Coordinate ({unit})", f"Hazard Y Coordinate ({unit})"])
        writer.writerows(hazardsList)
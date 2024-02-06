from H5toDataframe import convertAllH5Files
from filterFunctions import filterEasterEggs

velocityMissingCount = 0
dataframes = convertAllH5Files()
print(len(dataframes))
dataframes = filterEasterEggs(dataframes)
print(len(dataframes))

for name, (df, attrs) in dataframes.items():
    if not hasattr(df, 'velocity'):
        velocityMissingCount += 1
    # else:
        # print(f"{name}: DataFrame Shape: {df.shape}, Attributes: {attrs}")
        # print("First 5 lines of the columns:")
        # # print(df[['velocity', 'defect_channel', 'distance', 'magnetization', 'timestamp', 'wall_thickness']].head())
        # print(df.head())
        # print("\n")
print(f'Fehlende Velocity Werte: {velocityMissingCount}')


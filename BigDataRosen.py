from H5toDataframe import convertAllH5Files

velocityMissingCount = 0
all_dataframes = convertAllH5Files()

for name, (df, attrs) in all_dataframes.items():
    if not hasattr(df, 'velocity'):
        velocityMissingCount += 1
    else:
        print(f"{name}: DataFrame Shape: {df.shape}, Attributes: {attrs}")
        print("First 5 lines of the columns:")
        # print(df[['velocity', 'defect_channel', 'distance', 'magnetization', 'timestamp', 'wall_thickness']].head())
        print(df.head())
        print("\n")
print(f'Fehlende Velocity Werte: {velocityMissingCount}')


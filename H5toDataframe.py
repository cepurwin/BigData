import os
import pandas as pd
import h5py

def read_hdf5(file_path):
    """Read an HDF5 file into a Pandas DataFrame and return it along with attributes."""
    with h5py.File(file_path, 'r') as file:
        for keyname in file.keys():
            if keyname != "":
                data_group_name = keyname
            else:
                print(f"'data' missing in: {file_path}")
                return None, None

        data_group = file[data_group_name]
        data_dict = {name: data_group[name][:] for name in data_group.keys()}

        # Extract attributes
        attributes = {attr: data_group.attrs[attr] for attr in data_group.attrs.keys()}
        data_id = attributes.get('id', 'Unknown')

        max_length = max(len(values) for values in data_dict.values())
        shorter_columns = {name: len(values) for name, values in data_dict.items() if len(values) < max_length}
        if shorter_columns:
            # print(f"Inconsistency in: {data_id}")
            # for name, length in shorter_columns.items():
            #     print(f" - Column name:: {name}, Length: {length}")
            return None, attributes

        data_frame = pd.DataFrame(data_dict)
        return data_frame, attributes

def convertAllH5Files():
    all_dataframes = {}
    for file_name in os.listdir('datasetsRosen'):
        if file_name.endswith('.h5'):
            file_path = os.path.join('datasetsRosen', file_name)
            frame, frame_attrs = read_hdf5(file_path)
            if frame is not None:
                all_dataframes[file_name] = (frame, frame_attrs)
    return (all_dataframes)
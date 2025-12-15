import pandas as pd

def load_sheet(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a .xlsx or .csv file.")
    return df

def get_valid_list(prompt):
    vals = input(prompt)
    return [v.strip() for v in vals.split(",") if v.strip()]

def validate_sheet(df, config_col, swconfig_col, valid_configs, valid_swconfigs):
    errors = []
    for idx, row in df.iterrows():
        config = row.get(config_col)
        swconfig = row.get(swconfig_col)
        if config not in valid_configs or swconfig not in valid_swconfigs:
            errors.append({
                "Row": idx + 2,  # +2 for header and 0-based idx
                "ConfigName": config,
                "SoftwareConfig": swconfig
            })
    return errors

def main():
    print("=== Import Sheet Validator ===")
    file_path = input("Enter path to your import sheet (.xlsx or .csv): ").strip()
    df = load_sheet(file_path)
    print("Columns detected:")
    print(df.columns)

    # Ask user to specify column names for ConfigName and SoftwareConfig
    config_col = input("Enter the column name for ConfigName: ").strip()
    swconfig_col = input("Enter the column name for SoftwareConfig: ").strip()

    print("\nEnter valid ConfigName values (comma-separated, e.g., CAF4_S2,CAF1_S1):")
    valid_configs = get_valid_list("Valid ConfigName list: ")

    print("\nEnter valid SoftwareConfig values (comma-separated, e.g., A,B):")
    valid_swconfigs = get_valid_list("Valid SoftwareConfig list: ")

    error_rows = validate_sheet(df, config_col, swconfig_col, valid_configs, valid_swconfigs)

    print("\n=== Validation Report ===")
    if error_rows:
        print("Found rows with incorrect tags:")
        for err in error_rows:
            print(f"Row {err['Row']}: ConfigName={err['ConfigName']}, SoftwareConfig={err['SoftwareConfig']}")
    else:
        print("All testlines are correctly tagged!")

if __name__ == "__main__":
    main()

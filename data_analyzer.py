import pandas as pd
import sys

def _analyze_ventas_sheet(df_ventas):
    print("Analyzing 'VENTAS' sheet (Sales Data)...")
    ventas_results = {}

    if 'Precio Venta Real' in df_ventas.columns:
        ventas_results['total_sales'] = df_ventas['Precio Venta Real'].sum()
        ventas_results['average_sales_per_transaction'] = df_ventas['Precio Venta Real'].mean()
        ventas_results['total_transactions'] = len(df_ventas)
        print("Basic sales metrics calculated.")
    else:
        print("Error: 'Precio Venta Real' not found in 'VENTAS' sheet. Skipping basic sales metrics.")
        ventas_results['total_sales'] = 0
        ventas_results['average_sales_per_transaction'] = 0
        ventas_results['total_transactions'] = 0

    ventas_results['sales_by_vehicle_id'] = pd.Series(dtype=float)
    if 'ID_Vehículo' in df_ventas.columns and 'Precio Venta Real' in df_ventas.columns:
        ventas_results['sales_by_vehicle_id'] = df_ventas.groupby('ID_Vehículo')['Precio Venta Real'].sum().sort_values(ascending=False)
        print("Sales by Vehicle ID analyzed.")
    else: print("Warning: 'ID_Vehículo' or 'Precio Venta Real' not found in 'VENTAS' sheet. Cannot analyze sales by vehicle ID.")

    ventas_results['sales_by_channel'] = pd.Series(dtype=float)
    if 'Canal' in df_ventas.columns and 'Precio Venta Real' in df_ventas.columns:
        ventas_results['sales_by_channel'] = df_ventas.groupby('Canal')['Precio Venta Real'].sum().sort_values(ascending=False)
        print("Sales by Channel analyzed.")
    else: print("Warning: 'Canal' or 'Precio Venta Real' not found in 'VENTAS' sheet. Cannot analyze sales by channel.")

    ventas_results['sales_by_sede'] = pd.Series(dtype=float)
    if 'Sede' in df_ventas.columns and 'Precio Venta Real' in df_ventas.columns:
        ventas_results['sales_by_sede'] = df_ventas.groupby('Sede')['Precio Venta Real'].sum().sort_values(ascending=False)
        print("Sales by Location (Sede) analyzed.")
    else: print("Warning: 'Sede' or 'Precio Venta Real' not found in 'VENTAS' sheet. Cannot analyze sales by location.")

    ventas_results['sales_by_vendedor'] = pd.Series(dtype=float)
    if 'Vendedor' in df_ventas.columns and 'Precio Venta Real' in df_ventas.columns:
        ventas_results['sales_by_vendedor'] = df_ventas.groupby('Vendedor')['Precio Venta Real'].sum().sort_values(ascending=False)
        print("Sales by Salesperson (Vendedor) analyzed.")
    else: print("Warning: 'Vendedor' or 'Precio Venta Real' not found in 'VENTAS' sheet. Cannot analyze sales by salesperson.")

    ventas_results['total_profit'] = None
    if 'Precio Venta Real' in df_ventas.columns and 'Costo Vehículo' in df_ventas.columns:
        df_ventas['Profit'] = df_ventas['Precio Venta Real'] - df_ventas['Costo Vehículo']
        ventas_results['total_profit'] = df_ventas['Profit'].sum()
        print("Total Profit calculated.")
    else: print("Warning: 'Precio Venta Real' or 'Costo Vehículo' not found in 'VENTAS' sheet. Cannot calculate profit.")

    ventas_results['sales_over_time'] = pd.Series(dtype=float)
    if 'Fecha' in df_ventas.columns and 'Precio Venta Real' in df_ventas.columns:
        df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'], errors='coerce')
        df_ventas.dropna(subset=['Fecha'], inplace=True)
        if not df_ventas.empty:
            ventas_results['sales_over_time'] = df_ventas.set_index('Fecha')['Precio Venta Real'].resample('ME').sum()
            print("Sales trends over time analyzed.")
        else: print("Warning: No valid 'Fecha' entries after parsing in 'VENTAS' sheet. Skipping sales time series analysis.")
    else: print("Warning: 'Fecha' or 'Precio Venta Real' not found in 'VENTAS' sheet. Skipping sales time series analysis.")
    return ventas_results

def _analyze_vehiculos_sheet(df_vehiculos):
    print("\nAnalyzing 'VEHICULOS' sheet (Vehicle Inventory)...")
    vehiculos_results = {}

    vehiculos_results['total_vehicles'] = len(df_vehiculos)
    print(f"Total vehicles in inventory: {vehiculos_results['total_vehicles']}")

    vehiculos_results['vehicles_by_brand'] = pd.Series(dtype=int)
    if 'MARCA' in df_vehiculos.columns:
        vehiculos_results['vehicles_by_brand'] = df_vehiculos['MARCA'].value_counts()
        print("Vehicles by Brand analyzed.")
    else: print("Warning: 'MARCA' not found in 'VEHICULOS' sheet. Cannot analyze vehicles by brand.")

    vehiculos_results['vehicles_by_model'] = pd.Series(dtype=int)
    if 'MODELO' in df_vehiculos.columns:
        vehiculos_results['vehicles_by_model'] = df_vehiculos['MODELO'].value_counts()
        print("Vehicles by Model analyzed.")
    else: print("Warning: 'MODELO' not found in 'VEHICULOS' sheet. Cannot analyze vehicles by model.")

    vehiculos_results['vehicles_by_type'] = pd.Series(dtype=int)
    if 'TIPO VEHICULO' in df_vehiculos.columns:
        vehiculos_results['vehicles_by_type'] = df_vehiculos['TIPO VEHICULO'].value_counts()
        print("Vehicles by Type analyzed.")
    else: print("Warning: 'TIPO VEHICULO' not found in 'VEHICULOS' sheet. Cannot analyze vehicles by type.")

    vehiculos_results['vehicles_by_year'] = pd.Series(dtype=int)
    if 'AÑO' in df_vehiculos.columns:
        vehiculos_results['vehicles_by_year'] = df_vehiculos['AÑO'].value_counts().sort_index(ascending=False)
        print("Vehicles by Year analyzed.")
    else: print("Warning: 'AÑO' not found in 'VEHICULOS' sheet. Cannot analyze vehicles by year.")

    return vehiculos_results

def _analyze_nuevos_registros_sheet(df_nuevos_registros):
    print("\nAnalyzing 'NUEVOS REGISTROS' sheet (New Registrations)...")
    registros_results = {}
    registros_results['total_new_registrations'] = len(df_nuevos_registros)
    print(f"Total new registrations: {registros_results['total_new_registrations']}")

    registros_results['registrations_over_time'] = pd.Series(dtype=int)
    if 'Fecha' in df_nuevos_registros.columns:
        df_nuevos_registros['Fecha'] = pd.to_datetime(df_nuevos_registros['Fecha'], errors='coerce')
        df_nuevos_registros.dropna(subset=['Fecha'], inplace=True)
        if not df_nuevos_registros.empty:
            registros_results['registrations_over_time'] = df_nuevos_registros.set_index('Fecha').resample('ME').size()
            print("Registrations over Time analyzed.")
        else: print("Warning: No valid 'Fecha' entries after parsing in 'NUEVOS REGISTROS' sheet. Skipping time series analysis.")
    else: print("Warning: 'Fecha' not found in 'NUEVOS REGISTROS' sheet. Skipping time series analysis.")

    return registros_results

def analyze_data(all_dfs):
    if not all_dfs:
        print("No DataFrames provided for analysis. Exiting.")
        sys.exit(1)

    print("Performing comprehensive data analysis...")
    analysis_results = {}

    if 'VENTAS' in all_dfs and not all_dfs['VENTAS'].empty: analysis_results['ventas'] = _analyze_ventas_sheet(all_dfs['VENTAS'])
    else: print("Warning: 'VENTAS' sheet not found or is empty. Skipping sales analysis.")

    if 'VEHICULOS' in all_dfs and not all_dfs['VEHICULOS'].empty: analysis_results['vehiculos'] = _analyze_vehiculos_sheet(all_dfs['VEHICULOS'])
    else: print("Warning: 'VEHICULOS' sheet not found or is empty. Skipping vehicle analysis.")

    if 'NUEVOS REGISTROS' in all_dfs and not all_dfs['NUEVOS REGISTROS'].empty: analysis_results['nuevos_registros'] = _analyze_nuevos_registros_sheet(all_dfs['NUEVOS REGISTROS'])
    else: print("Warning: 'NUEVOS REGISTROS' sheet not found or is empty. Skipping new registrations analysis.")

    print("\nComprehensive data analysis completed.")
    return analysis_results
import os
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def _generate_sales_text_section(ventas_data):
    report_section = "--- Sales Overview (VENTAS) ---\n"
    report_section += f"Total Sales: ${ventas_data['total_sales']:.2f}\n"
    report_section += f"Average Sales per Transaction: ${ventas_data['average_sales_per_transaction']:.2f}\n"
    report_section += f"Total Number of Transactions: {ventas_data['total_transactions']}\n\n"
    if not ventas_data['sales_by_vehicle_id'].empty:
        report_section += "Top 5 Sales by Vehicle ID:\n"
        for vehicle_id, sales in ventas_data['sales_by_vehicle_id'].head(5).items():
            report_section += f"- Vehicle ID {vehicle_id}: ${sales:.2f}\n"
    else: report_section += "No sales by vehicle ID data available.\n"

    if not ventas_data['sales_by_channel'].empty:
        report_section += "\nTop 5 Sales by Channel:\n"
        for channel, sales in ventas_data['sales_by_channel'].head(5).items():
            report_section += f"- {channel}: ${sales:.2f}\n"
    else: report_section += "No sales by channel data available.\n"

    if not ventas_data['sales_by_sede'].empty:
        report_section += "\nTop 5 Sales by Location (Sede):\n"
        for sede, sales in ventas_data['sales_by_sede'].head(5).items():
            report_section += f"- {sede}: ${sales:.2f}\n"
    else: report_section += "No sales by location data available.\n"

    if not ventas_data['sales_by_vendedor'].empty:
        report_section += "\nTop 5 Sales by Salesperson (Vendedor):\n"
        for vendedor, sales in ventas_data['sales_by_vendedor'].head(5).items():
            report_section += f"- {vendedor}: ${sales:.2f}\n"
    else: report_section += "No sales by salesperson data available.\n"

    if ventas_data['total_profit'] is not None: report_section += f"\nTotal Estimated Profit: ${ventas_data['total_profit']:.2f}\n"
    else: report_section += "Total estimated profit not available.\n"

    if not ventas_data['sales_over_time'].empty:
        report_section += "\nSales Over Time (Monthly):\n"
        for date, sales in ventas_data['sales_over_time'].items():
            report_section += f"- {date.strftime('%Y-%m')}: ${sales:.2f}\n"
    else: report_section += "No sales over time data available.\n"
    report_section += "\n"
    return report_section

def _generate_vehiculos_text_section(vehiculos_data):
    report_section = "--- Vehicle Inventory Overview (VEHICULOS) ---\n"
    report_section += f"Total Vehicles in Inventory: {vehiculos_data['total_vehicles']}\n\n"

    if not vehiculos_data['vehicles_by_brand'].empty:
        report_section += "Top 5 Vehicles by Brand:\n"
        for brand, count in vehiculos_data['vehicles_by_brand'].head(5).items():
            report_section += f"- {brand}: {count} units\n"
    else: report_section += "No vehicle by brand data available.\n"

    if not vehiculos_data['vehicles_by_model'].empty:
        report_section += "\nTop 5 Vehicles by Model:\n"
        for model, count in vehiculos_data['vehicles_by_model'].head(5).items():
            report_section += f"- {model}: {count} units\n"
    else: report_section += "No vehicle by model data available.\n"

    if not vehiculos_data['vehicles_by_type'].empty:
        report_section += "\nVehicles by Type:\n"
        for v_type, count in vehiculos_data['vehicles_by_type'].head(5).items():
            report_section += f"- {v_type}: {count} units\n"
    else: report_section += "No vehicle by type data available.\n"

    if not vehiculos_data['vehicles_by_year'].empty:
        report_section += "\nVehicles by Year:\n"
        for year, count in vehiculos_data['vehicles_by_year'].head(5).items():
            report_section += f"- {int(year)}: {count} units\n"
    else: report_section += "No vehicle by year data available.\n"
    report_section += "\n"
    return report_section

def _generate_nuevos_registros_text_section(registros_data):
    report_section = "--- New Registrations Overview (NUEVOS REGISTROS) ---\n"
    report_section += f"Total New Registrations: {registros_data['total_new_registrations']}\n\n"
    if not registros_data['registrations_over_time'].empty:
        report_section += "\nNew Registrations Over Time (Monthly):\n"
        for date, count in registros_data['registrations_over_time'].items():
            report_section += f"- {date.strftime('%Y-%m')}: {count} registrations\n"
    else: report_section += "No registrations over time data available.\n"
    report_section += "\n"
    return report_section

def generate_text_report(analysis_results, output_folder, file_name):
    if not analysis_results:
        print("No analysis results available to generate a text report.")
        return None
    full_path = os.path.join(output_folder, file_name)
    doc = SimpleDocTemplate(full_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    code_style = ParagraphStyle('Code', parent=styles['Code'], fontName='Courier', fontSize=10, leading=12)
    story.append(Paragraph("Comprehensive Business Analysis Report", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))
    if 'ventas' in analysis_results:
        story.append(Paragraph("Sales Overview (VENTAS)", styles['h2']))
        story.append(Paragraph(_generate_sales_text_section(analysis_results['ventas']).replace('\n', '<br/>'), code_style))
        story.append(Spacer(1, 0.2 * inch))
    if 'vehiculos' in analysis_results:
        story.append(Paragraph("Vehicle Inventory Overview (VEHICULOS)", styles['h2']))
        story.append(Paragraph(_generate_vehiculos_text_section(analysis_results['vehiculos']).replace('\n', '<br/>'), code_style))
        story.append(Spacer(1, 0.2 * inch))
    if 'nuevos_registros' in analysis_results:
        story.append(Paragraph("New Registrations Overview (NUEVOS REGISTROS)", styles['h2']))
        story.append(Paragraph(_generate_nuevos_registros_text_section(analysis_results['nuevos_registros']).replace('\n', '<br/>'), code_style))
        story.append(Spacer(1, 0.2 * inch))
    try:
        doc.build(story)
        print(f"Comprehensive text report saved as PDF to '{full_path}'.")
        return full_path
    except Exception as e:
        print(f"Error saving text report as PDF to '{full_path}': {e}")
        return None

def _create_sales_without_igv_by_sede_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data.get('sales_without_igv_by_sede', pd.Series()).empty:
        plt.figure(figsize=(10, 6))
        ventas_data['sales_without_igv_by_sede'].plot(kind='bar', color='darkorange')
        plt.title('Ventas sin IGV por Sede (Suma)', fontsize=16)
        plt.xlabel('Sede', fontsize=12)
        plt.ylabel('Ventas sin IGV ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        img_path = os.path.join(output_folder, f"{base_image_name}_sales_without_igv_by_sede{extension}")
        try:
            plt.savefig(img_path)
            return img_path
        finally: plt.close()
    return None
def _create_sales_by_vehicle_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data['sales_by_vehicle_id'].empty:
        plt.figure(figsize=(12, 7))
        top_10_sales = ventas_data['sales_by_vehicle_id'].head(10)
        top_10_sales.plot(kind='bar', color='skyblue')
        plt.title('Top 10 Sales by Vehicle ID', fontsize=16)
        plt.xlabel('Vehicle ID', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        img_path = os.path.join(output_folder, f"{base_image_name}_sales_by_vehicle{extension}")
        try:
            plt.savefig(img_path)
            print(f"Visual report saved: '{img_path}'.")
            return img_path
        except Exception as e:
            print(f"Error saving visual report '{img_path}': {e}")
            return None
        finally: plt.close()
    return None

def _create_sales_by_channel_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data['sales_by_channel'].empty:
        plt.figure(figsize=(10, 6))
        top_channels = ventas_data['sales_by_channel'].head(5)
        top_channels.plot(kind='bar', color='lightgreen')
        plt.title('Top 5 Sales by Channel', fontsize=16)
        plt.xlabel('Sales Channel', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        img_path = os.path.join(output_folder, f"{base_image_name}_sales_by_channel{extension}")
        try:
            plt.savefig(img_path)
            print(f"Visual report saved: '{img_path}'.")
            return img_path
        except Exception as e:
            print(f"Error saving visual report '{img_path}': {e}")
            return None
        finally: plt.close()
    return None

# Dentro de report_generator.py
def _create_top_selling_models_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data.get('top_selling_models', pd.Series()).empty:
        plt.figure(figsize=(10, 6))
        # Gráfico de barras horizontales (barh)
        ventas_data['top_selling_models'].sort_values().plot(kind='barh', color='darkcyan')
        plt.title('Top 5 Modelos de Vehículos más Vendidos (Conteo)', fontsize=16)
        plt.xlabel('Cantidad de Ventas', fontsize=12)
        plt.ylabel('Modelo', fontsize=12)
        plt.tight_layout()
        img_path = os.path.join(output_folder, f"{base_image_name}_top_selling_models{extension}")
        try:
            plt.savefig(img_path)
            return img_path
        finally: plt.close()
    return None

# Dentro de report_generator.py (modificación o nueva función)
def _create_sales_count_by_channel_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data.get('sales_count_by_channel', pd.Series()).empty:
        plt.figure(figsize=(10, 6))
        ventas_data['sales_count_by_channel'].head(5).plot(kind='bar', color='lightgreen')
        plt.title('Top 5 Canales con más Ventas (Conteo)', fontsize=16)
        plt.xlabel('Canal de Venta', fontsize=12)
        plt.ylabel('Cantidad de Ventas', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        img_path = os.path.join(output_folder, f"{base_image_name}_sales_count_by_channel{extension}")
        try:
            plt.savefig(img_path)
            return img_path
        finally: plt.close()
    return None

# Dentro de report_generator.py
def _create_client_segmentation_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data.get('client_segmentation_without_igv', pd.Series()).empty:
        plt.figure(figsize=(10, 10))
        # Gráfico circular (pie)
        plt.pie(ventas_data['client_segmentation_without_igv'], 
                labels=ventas_data['client_segmentation_without_igv'].index, 
                autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
        plt.title('Segmento de Clientes por Ventas sin IGV', fontsize=16)
        plt.axis('equal') # Asegura que el gráfico sea un círculo
        plt.tight_layout()
        img_path = os.path.join(output_folder, f"{base_image_name}_client_segmentation{extension}")
        try:
            plt.savefig(img_path)
            return img_path
        finally: plt.close()
    return None

def _create_sales_over_time_chart(ventas_data, output_folder, base_image_name, extension):
    if not ventas_data['sales_over_time'].empty:
        plt.figure(figsize=(12, 6))
        ventas_data['sales_over_time'].plot(kind='line', marker='o', color='darkblue')
        plt.title('Monthly Sales Trend', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.7)
        img_path = os.path.join(output_folder, f"{base_image_name}_sales_over_time{extension}")
        try:
            plt.savefig(img_path)
            print(f"Visual report saved: '{img_path}'.")
            return img_path
        except Exception as e:
            print(f"Error saving visual report '{img_path}': {e}")
            return None
        finally: plt.close()
    return None

def _create_vehicles_by_brand_chart(vehiculos_data, output_folder, base_image_name, extension):
    if not vehiculos_data['vehicles_by_brand'].empty:
        plt.figure(figsize=(10, 6))
        top_brands = vehiculos_data['vehicles_by_brand'].head(10)
        top_brands.plot(kind='bar', color='lightcoral')
        plt.title('Top 10 Vehicles by Brand', fontsize=16)
        plt.xlabel('Brand', fontsize=12)
        plt.ylabel('Number of Vehicles', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        img_path = os.path.join(output_folder, f"{base_image_name}_vehicles_by_brand{extension}")
        try:
            plt.savefig(img_path)
            print(f"Visual report saved: '{img_path}'.")
            return img_path
        except Exception as e:
            print(f"Error saving visual report '{img_path}': {e}")
            return None
        finally: plt.close()
    return None

def _create_vehicles_by_type_chart(vehiculos_data, output_folder, base_image_name, extension):
    if not vehiculos_data['vehicles_by_type'].empty:
        plt.figure(figsize=(10, 6))
        top_types = vehiculos_data['vehicles_by_type'].head(5)
        top_types.plot(kind='bar', color='gold')
        plt.title('Top 5 Vehicles by Type', fontsize=16)
        plt.xlabel('Vehicle Type', fontsize=12)
        plt.ylabel('Number of Vehicles', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        img_path = os.path.join(output_folder, f"{base_image_name}_vehicles_by_type{extension}")
        try:
            plt.savefig(img_path)
            print(f"Visual report saved: '{img_path}'.")
            return img_path
        except Exception as e:
            print(f"Error saving visual report '{img_path}': {e}")
            return None
        finally: plt.close()
    return None

def _create_registrations_over_time_chart(registros_data, output_folder, base_image_name, extension):
    if not registros_data['registrations_over_time'].empty:
        plt.figure(figsize=(12, 6))
        registros_data['registrations_over_time'].plot(kind='line', marker='o', color='forestgreen')
        plt.title('New Registrations Over Time (Monthly)', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Registrations', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.7)
        img_path = os.path.join(output_folder, f"{base_image_name}_registrations_over_time{extension}")
        try:
            plt.savefig(img_path)
            print(f"Visual report saved: '{img_path}'.")
            return img_path
        except Exception as e:
            print(f"Error saving visual report '{img_path}': {e}")
            return None
        finally: plt.close()
    return None

def generate_visual_report(analysis_results, output_folder, base_image_name, extension):
    image_paths = []

    if 'ventas' in analysis_results:
        ventas_data = analysis_results['ventas']
        chart_path = _create_sales_by_vehicle_chart(ventas_data, output_folder, base_image_name, extension)
        if chart_path: image_paths.append(chart_path)

        chart_path = _create_sales_by_channel_chart(ventas_data, output_folder, base_image_name, extension)
        if chart_path: image_paths.append(chart_path)

        chart_path = _create_sales_over_time_chart(ventas_data, output_folder, base_image_name, extension)
        if chart_path: image_paths.append(chart_path)

        path = _create_sales_without_igv_by_sede_chart(ventas_data, output_folder, base_image_name, extension)
        if path: image_paths.append(path)

        path = _create_top_selling_models_chart(ventas_data, output_folder, base_image_name, extension)
        if path: image_paths.append(path)
        
        path = _create_sales_count_by_channel_chart(ventas_data, output_folder, base_image_name, extension)
        if path: image_paths.append(path)
        
        path = _create_client_segmentation_chart(ventas_data, output_folder, base_image_name, extension)
        if path: image_paths.append(path)

    if 'vehiculos' in analysis_results:
        vehiculos_data = analysis_results['vehiculos']
        chart_path = _create_vehicles_by_brand_chart(vehiculos_data, output_folder, base_image_name, extension)
        if chart_path: image_paths.append(chart_path)

        chart_path = _create_vehicles_by_type_chart(vehiculos_data, output_folder, base_image_name, extension)
        if chart_path: image_paths.append(chart_path)

    if 'nuevos_registros' in analysis_results:
        registros_data = analysis_results['nuevos_registros']
        chart_path = _create_registrations_over_time_chart(registros_data, output_folder, base_image_name, extension)
        if chart_path: image_paths.append(chart_path)

    print("All visual reports generated.")
    return image_paths
import pandas as pd
from core.rubros.models import Rubro
from core.activities.models import Activity
from core.tasks.models import Task
from rest_framework.exceptions import APIException


class BudgetProcessor:
    def __init__(self, file, project):
        self.file = file
        self.project = project

    def process(self):
        try:
            # Intentar leer el archivo Excel
            df = pd.read_excel(self.file, header=None)

            # Verificar que las filas contengan los valores esperados ("RUBRO" y "TOTAL")
            rubro_row, total_row = None, None
            for index, row in df.iterrows():
                if "RUBRO" in row.values:
                    rubro_row = index
                if "TOTAL" in row.values:
                    total_row = index

            if rubro_row is None or total_row is None:
                raise InvalidFileFormatError(
                    "El archivo no contiene los encabezados 'RUBRO' o 'TOTAL'."
                )

            # Procesar las filas entre "RUBRO" y "TOTAL"
            for index in range(rubro_row + 1, total_row):
                rubro = df.iloc[index, 2]  # Columna con el nombre del rubro
                total = df.iloc[index, 42]  # Columna con el valor total del rubro

                # Limpiar el valor de total
                total = str(total).replace("$", "").replace(" ", "").replace(",", "")

                if pd.isna(rubro) or rubro == "":
                    continue

                try:
                    total = float(total)
                except ValueError:
                    total = 0.0  # Si el valor no se puede convertir a float, asignar 0

                try:
                    print("rubro", rubro, "total", total)
                    Rubro.objects.create(
                        descripcion=rubro,
                        value_sgr=total,
                        project=self.project,
                    )
                except Exception as db_error:
                    raise DatabaseError(f"Error al guardar el rubro: {str(db_error)}")

        except InvalidFileFormatError as e:
            raise e  # Propagar el error de formato de archivo
        except DatabaseError as e:
            raise e  # Propagar el error relacionado con la base de datos
        except Exception as e:
            # Cualquier otro error inesperado
            raise APIException(
                f"Error inesperado al procesar el archivo de presupuesto: {str(e)}"
            )


class ActivitiesProcessor:
    def __init__(self, file, project):
        self.file = file
        self.project = project

    def process(self):
        try:
            # Leer el archivo Excel
            df = pd.read_excel(self.file, sheet_name="Matriz de Formulación", header=1)

            # Filtrar las columnas necesarias
            columnas_deseadas = [
                "Actividades",
                "Num_tarea",
                "Tareas",
                "Responsable (Entidad)",
                "Personal requerido (perfiles y descripción)",
                "Resultados de la actividad",
            ]
            columnas_presentes = [col for col in columnas_deseadas if col in df.columns]
            df_filtrado = df[columnas_presentes]

            # Limpiar el JSON usando la lógica de salida que ya definiste
            actividades_limpias = self.limpiar_json_con_condicion_de_salida(df_filtrado)

            # Crear las actividades y tareas en la base de datos
            for actividad_data in actividades_limpias:
                # Crear la actividad
                actividad = Activity.objects.create(
                    name=actividad_data["actividad"],
                    project=self.project,
                    start_date=None,
                    end_date=None,
                    state="Pendiente",
                )

                # Crear las tareas relacionadas con la actividad
                for tarea_data in actividad_data["tareas"]:
                    Task.objects.create(
                        task_num=tarea_data["num_tarea"],
                        name=tarea_data["nombre"],
                        start_date=None,
                        end_date=None,
                        activity=actividad,
                        state="Pendiente",
                    )

        except InvalidFileFormatError as e:
            raise e  # Propagar el error de formato de archivo
        except DatabaseError as e:
            raise e  # Propagar el error relacionado con la base de datos
        except Exception as e:
            # Cualquier otro error inesperado
            raise APIException(
                f"Error inesperado al procesar el archivo de actividades: {str(e)}"
            )

    def limpiar_json_con_condicion_de_salida(self, df):
        actividades_filtradas = []
        actividad_actual = None
        tareas_filtradas = []

        # Recorremos el dataframe fila por fila
        for i in range(len(df)):
            actividad = df.iloc[i, 0]  # Obtener el nombre de la actividad
            num_tarea = df.iloc[i, 1]  # Obtener el número de tarea
            nombre_tarea = df.iloc[i, 2]  # Obtener el nombre de la tarea

            # Si tanto la actividad, el número de tarea y el nombre de la tarea son NaN, es el final
            if pd.isna(actividad) and pd.isna(num_tarea) and pd.isna(nombre_tarea):
                break

            # Si la actividad cambia, es una nueva actividad
            if not pd.isna(actividad):
                if actividad_actual is not None and tareas_filtradas:
                    actividades_filtradas.append(
                        {"actividad": actividad_actual, "tareas": tareas_filtradas}
                    )
                actividad_actual = actividad
                tareas_filtradas = []  # Resetear tareas para la nueva actividad

            # Si el número de tarea y nombre no son NaN, agregamos la tarea
            if not pd.isna(num_tarea) and not pd.isna(nombre_tarea):
                tareas_filtradas.append(
                    {"num_tarea": num_tarea, "nombre": nombre_tarea}
                )

        # Agregar la última actividad si hay tareas filtradas
        if actividad_actual is not None and tareas_filtradas:
            actividades_filtradas.append(
                {"actividad": actividad_actual, "tareas": tareas_filtradas}
            )

        return actividades_filtradas


class InvalidFileFormatError(APIException):
    status_code = 400
    default_detail = "Formato de archivo inválido."
    default_code = "invalid_file_format"


class DatabaseError(APIException):
    status_code = 500
    default_detail = "Error interno al guardar el rubro en la base de datos."
    default_code = "database_error"

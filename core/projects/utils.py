import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from core.rubros.models import Rubro
from core.activities.models import Activity
from core.tasks.models import Task
from core.counterparts.models import Counterpart
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


class CounterPartsProcessor:
    def __init__(self, file, project):
        self.file = file
        self.project = project

    def process(self):
        try:
            # Leer el archivo Excel
            resumen_data = pd.read_excel(self.file, sheet_name="RESUMEN", header=None)

            # Eliminar las primeras 6 filas
            resumen_data_cleaned = resumen_data.drop(
                index=[0, 1, 2, 3, 4, 5, 6]
            ).reset_index(drop=True)

            # Fusionar las primeras dos filas restantes para crear un encabezado coherente
            new_header = (
                resumen_data_cleaned.iloc[0].fillna("")
                + "_"
                + resumen_data_cleaned.iloc[1].fillna("")
            )
            new_header = new_header.str.replace("_$", "", regex=True)
            resumen_data_cleaned.columns = new_header

            # Limpiar el DataFrame
            resumen_data_cleaned = resumen_data_cleaned[2:].reset_index(drop=True)
            resumen_data_cleaned = resumen_data_cleaned.iloc[
                :, 3:-1
            ]  # Eliminar primeras 3 y última columna
            resumen_data_cleaned.columns = resumen_data_cleaned.columns.str.lstrip(
                "_"
            ).str.replace("CONTRAPARTIDA_", "", regex=False)

            # Validar el proyecto
            if not self.project:
                raise ValueError("El proyecto no es válido o no está asignado.")
            print(f"Procesando contrapartidas para el proyecto: {self.project.name}")

            # Procesar contrapartidas
            for i in range(0, len(resumen_data_cleaned.columns) - 1, 2):
                entidad = resumen_data_cleaned.columns[i]

                if pd.isna(entidad) or entidad.strip() == "":
                    print(f"Entidad vacía o inválida en la columna {i}, saltando.")
                    continue

                # Recuperar los valores de especie y efectivo
                especie = resumen_data_cleaned.iloc[1, i]
                efectivo = resumen_data_cleaned.iloc[1, i + 1]

                # Validar y limpiar los valores
                especie = self.limpiar_valor(especie)
                efectivo = self.limpiar_valor(efectivo)

                # Validar si los valores son válidos antes de guardar
                if especie is None or efectivo is None:
                    print(f"Valores inválidos para la entidad {entidad}, saltando.")
                    continue

                # Verificar si la entidad es válida
                if pd.isna(entidad) or entidad.strip() == "":
                    print("Entidad vacía para la contrapartida, saltando creación.")
                    continue

                try:
                    # Crear la contrapartida en la base de datos
                    print(f"Creando contrapartida para la entidad: {entidad}")
                    Counterpart.objects.create(
                        project=self.project,
                        name=entidad,
                        value_species=especie,
                        value_chash=efectivo,
                    )
                except Exception as db_error:
                    raise DatabaseError(
                        f"Error al guardar la contrapartida para la entidad {entidad}: {str(db_error)}"
                    )

        except InvalidFileFormatError as e:
            raise e  # Propagar el error de formato de archivo
        except DatabaseError as e:
            raise e  # Propagar el error relacionado con la base de datos
        except Exception as e:
            # Cualquier otro error inesperado
            raise APIException(
                f"Error inesperado al procesar el archivo de presupuesto para contrapartidas: {str(e)}"
            )

    def limpiar_valor(self, valor):
        """
        Limpia el valor (eliminando símbolos de dólar, comas, espacios) y lo convierte a float.
        Si el valor es inválido, devuelve None.
        """
        try:
            # Convertir a string y limpiar caracteres no numéricos
            cleaned_value = str(valor).replace("$", "").replace(",", "").strip()
            if cleaned_value == "" or pd.isna(valor):
                return None
            return float(cleaned_value)
        except ValueError:
            print(f"Valor inválido al intentar convertir: {valor}")
            return None


class ActivitiesProcessor:
    def __init__(self, file, project):
        self.file = file
        self.project = project

    def process(self):
        try:
            # Leer el archivo Excel
            df = pd.read_excel(self.file, sheet_name="Matriz de Formulación", header=1)
            dfc = pd.read_excel(self.file, sheet_name="Cronograma", header=0)

            fecha_base = self.convertir_fecha_base(self.project.start_date)

            dfc[["start_date", "end_date"]] = dfc.apply(
                lambda row: self.calcular_fechas(row, fecha_base),
                axis=1,
                result_type="expand",
            )

            # Asegúrate de que las columnas start_date y end_date no tengan valores nulos o None
            dfc["start_date"] = dfc["start_date"].fillna(pd.NaT)
            dfc["end_date"] = dfc["end_date"].fillna(pd.NaT)

            columnas_deseadas_cronograma = [
                "DURACION",
                "DESDE",
                "HASTA",
                "start_date",
                "end_date",
            ]

            # Filtrar las columnas necesarias
            columnas_deseadas = [
                "Actividades",
                "Num_tarea",
                "Tareas",
                "Responsable (Entidad)",
                "Personal requerido (perfiles y descripción)",
                "Resultados de la actividad",
            ]
            columnas_presentes_cronograma = [
                colC for colC in columnas_deseadas_cronograma if colC in dfc.columns
            ]
            columnas_presentes = [col for col in columnas_deseadas if col in df.columns]
            df_filtrado = df[columnas_presentes]
            df_filtrado_cronograma = dfc[columnas_presentes_cronograma]

            # Limpiar el JSON usando la lógica de salida que ya definiste
            actividades_limpias = self.limpiar_json_con_condicion_de_salida(
                df_filtrado, df_filtrado_cronograma
            )

            # Crear las actividades y tareas en la base de datos
            for actividad_data in actividades_limpias:
                # Crear la actividad
                actividad = Activity.objects.create(
                    name=actividad_data["actividad"],
                    project=self.project,
                    start_date=actividad_data["start_date"],
                    end_date=actividad_data["end_date"],
                    duration=actividad_data["duration"],
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

    def limpiar_json_con_condicion_de_salida(self, df, dfc):
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
        for i, actividad in enumerate(actividades_filtradas):
            # Extraemos el start_date y end_date de dfC usando el índice i
            fechas = dfc.iloc[i][
                ["start_date", "end_date", "DURACION"]
            ]  # Esto se hace por índice de dfC
            actividad["start_date"] = str(fechas["start_date"])
            actividad["end_date"] = str(fechas["end_date"])
            actividad["duration"] = int(fechas["DURACION"])

        return actividades_filtradas

    def convertir_fecha_base(self, fecha_base):
        """
        Convierte una fecha (datetime.date o datetime.datetime o str) a un objeto datetime.datetime.
        Si es un datetime.date, la hora será 00:00:00. Si es una cadena (str), se intentará convertirla.
        """

        fecha_datetime = datetime.strptime(fecha_base, "%Y-%m-%d")

        return fecha_datetime

    def calcular_fechas(self, row, fecha_base):
        try:
            # Asegúrate de que fecha_base es un objeto datetime válido
            if not isinstance(fecha_base, datetime):
                raise ValueError("fecha_base debe ser un objeto datetime")

            # Convertir "DESDE" y "DURACION" a números si no lo son
            desde = pd.to_numeric(row["DESDE"], errors="coerce")
            duracion = pd.to_numeric(row["DURACION"], errors="coerce")

            # Verificar que los valores no sean NaN o None
            if pd.isna(desde) or pd.isna(duracion):
                return pd.NaT, pd.NaT  # Devolvemos NaT si hay valores faltantes

            # Calcular las fechas
            if desde == 1:
                start_date = fecha_base
                end_date = start_date + relativedelta(months=int(duracion))
            else:
                start_date = fecha_base + relativedelta(months=int(desde) - 1)
                end_date = start_date + relativedelta(months=int(duracion))

            # Asegúrate de que las fechas sean de tipo datetime.date
            if isinstance(start_date, datetime):
                start_date = start_date.date()
            if isinstance(end_date, datetime):
                end_date = end_date.date()

            return start_date, end_date

        except Exception as e:
            print(f"Error en calcular_fechas: {str(e)}")
            return pd.NaT, pd.NaT  # Devolvemos pd.NaT si hay un error


class InvalidFileFormatError(APIException):
    status_code = 400
    default_detail = "Formato de archivo inválido."
    default_code = "invalid_file_format"


class DatabaseError(APIException):
    status_code = 500
    default_detail = "Error interno al guardar el rubro en la base de datos."
    default_code = "database_error"

import pandas as pd
from core.rubros.models import Rubro
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


class InvalidFileFormatError(APIException):
    status_code = 400
    default_detail = "Formato de archivo inválido."
    default_code = "invalid_file_format"


class DatabaseError(APIException):
    status_code = 500
    default_detail = "Error interno al guardar el rubro en la base de datos."
    default_code = "database_error"

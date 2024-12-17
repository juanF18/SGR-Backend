from io import BytesIO
from xhtml2pdf import pisa
from django.utils import timezone


class GeneratePdf:
    """
    Class to generate a PDF file with the data of a CDP (Certificado de Disponibilidad Presupuestal)
    """

    def __init__(self, entity, user, dataCdp):
        self.entity = entity
        self.user = user
        self.dataCdp = dataCdp

    def generate_pdf(self):
        html = self.metaData()

        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html.encode("utf-8"), dest=buffer)

        buffer.seek(0)
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    def metaData(self):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Generar PDF</title>
            <style>
                @page {{
                    size: letter;
                    margin: 2cm;
                    font-family: Arial, sans-serif !important; 
                }}
                header {{
                    font-size: 12px;
                    align-items: center;
                }}
                .table-header,
                .table-footer {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .td-header.no-spacing h1{{
                    font-size: 16px;
                }}
                .td-header.no-spacing h1, 
                .td-header.no-spacing p {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <header>
                {self.headerPdf()}
            </header>
            <main>
                {self.bodyPdf()}
            </main>
            <footer>
                {self.footerPdf()}
            </footer>
        </body>
        </html>
        """
        return html

    def headerPdf(self):
        html = f"""
        <header>
            <table class="table-header">
                <tr>
                    <td class="td-header" style="width: 100%; text-align: center;">
                        <h1>{self.entity.name}</h1>
                        <p>{self.entity.nit}</p>
                        <p>{self.entity.address}</p>
                        <p>{self.entity.phone}</p>
                        <p>{self.entity.email}</p>
                    </td>
                </tr>
            </table>
        </header>
        """
        return html

    def footerPdf(self):
        html = f"""
        <footer>
            <table class="table-footer">
                <tr>
                    <td class="td-footer" style="width: 20%; text-align: left;">
                        <p>Desarrollo</p>
                    </td>
                    <td class="td-footer" style="width: 20%; text-align: center;">
                        <p>Impresión {timezone.localdate().strftime('%d/%m/%Y')}</p>
                    </td>
                    <td class="td-footer" style="width: 40%; text-align: center;">
                        <p>Usuario: {self.user.name} {self.user.last_name}</p>
                    </td>
                    <td class="td-footer" style="width: 20%; text-align: right;">
                        <p>Pagina: 1 de 1 </p>
                    </td>
                </tr>
        </footer>
        """
        return html

    def bodyPdf(self):
        html = f"""
        <section>
            <h2 style="text-align: center;">Certificado de Disponibilidad Presupuestal (CDP)</h2>
            
            <div style="margin-bottom: 20px;">
                <strong>Número:</strong> {self.dataCdp.number if self.dataCdp.number else 'No asignado'} <br>
                <strong>Fecha de Expedición:</strong> {self.dataCdp.expedition_date.strftime('%d/%m/%Y') if self.dataCdp.expedition_date else 'No asignada'} <br>
                <strong>Monto:</strong> {self.dataCdp.amount if self.dataCdp.amount else 'No especificado'} <br>
            </div>

            <div style="margin-bottom: 20px;">
                <strong>Descripción:</strong> <br>
                <p>{self.dataCdp.description if self.dataCdp.description else 'No especificada'}</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <strong>Rubro:</strong> {self.dataCdp.rubro.descripcion if self.dataCdp.rubro else 'No asignado'} <br>
            </div>
            
            <div style="margin-bottom: 20px;">
                <strong>Estado:</strong> 
                <ul>
                    <li><strong>Generado:</strong> {"Sí" if self.dataCdp.is_generated else "No"}</li>
                    <li><strong>Cancelado:</strong> {"Sí" if self.dataCdp.is_canceled else "No"}</li>
                </ul>
            </div>

            <hr style="border: 1px solid #ccc;">
        </section>
        """
        return html

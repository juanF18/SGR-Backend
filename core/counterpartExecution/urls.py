from django.urls import path
from .views import CounterpartExecutionView, CounterpartExecutionDetailView

urlpatterns = [
    # URL para listar y crear ejecuciones de contrapartidas
    path(
        "counterpart-executions/",
        CounterpartExecutionView.as_view(),
        name="counterpart-executions",
    ),
    # URL para obtener, actualizar y eliminar una ejecución específica
    path(
        "counterpart-executions/<uuid:execution_id>/",
        CounterpartExecutionDetailView.as_view(),
        name="counterpart-execution-detail",
    ),
]

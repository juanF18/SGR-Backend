from django.db import models
from core.cdps.models import Cdps


# Create your models here.
class Contract(models.Model):
    contract_number = models.CharField(
        "contract_number", max_length=100, null=True, blank=True
    )
    contracting_nit = models.CharField(
        "contracting_nit", max_length=100, null=True, blank=True
    )
    contracted_nit = models.CharField(
        "contracted_nit", max_length=100, null=True, blank=True
    )
    contracting_name = models.CharField(
        "contracting_name", max_length=100, null=True, blank=True
    )
    start_date = models.DateField("start_date", null=True, blank=True)
    end_date = models.DateField("end_date", null=True, blank=True)
    contract_info = models.TextField("contract_info", null=True, blank=True)
    amount = models.DecimalField(
        "amount", max_digits=10, decimal_places=2, null=True, blank=True
    )
    supervisor_name = models.CharField(
        "supervisor_name", max_length=100, null=True, blank=True
    )
    supervisor_identification = models.CharField(
        "supervisor_identification", max_length=100, null=True, blank=True
    )
    contract_url = models.CharField(
        "contract_url", max_length=100, null=True, blank=True
    )
    observations = models.TextField("observations", null=True, blank=True)
    cpds_id = models.ForeignKey(Cdps, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "contracts"
        ordering = ["id"]

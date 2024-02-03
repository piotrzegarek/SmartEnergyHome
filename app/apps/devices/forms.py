from django.forms import ChoiceField, ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _

from .enums import EnergyUnit, PlanPeriod
from .models import ConsumeEnergyDevice, ProduceEnergyDevice, StoreEnergyDevice


class BaseDeviceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get("user"):
            self.user = kwargs.get("user")
            kwargs.pop("user")
        super(BaseDeviceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].widget.attrs.update({"autocomplete": "off"})

    def clean_name(self):
        name = self.cleaned_data["name"]

        if self._meta.model.objects.filter(name=name, user=self.user).exists():
            raise ValidationError("Device with this name already exists.")

        return name


class BaseDeviceMeta:
    exclude = ["user", "enabled"]


class ConsumeEnergyForm(BaseDeviceForm):
    class Meta(BaseDeviceMeta):
        model = ConsumeEnergyDevice
        error_messages = {
            "period_execution": {
                "min_value": _("The minimum plan execution count must be grater than 0")
            },
            "energy_consumption": {
                "min_value": _("Energy consumption can't be lower than 0")
            },
        }

    plan_period = ChoiceField(choices=PlanPeriod.choices())
    energy_unit = ChoiceField(choices=EnergyUnit.choices())


class StoreEnergyForm(BaseDeviceForm):
    class Meta(BaseDeviceMeta):
        model = StoreEnergyDevice


class ProduceEnergyForm(BaseDeviceForm):
    class Meta(BaseDeviceMeta):
        model = ProduceEnergyDevice

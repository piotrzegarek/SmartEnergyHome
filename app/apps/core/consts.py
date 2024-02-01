from .enums import DeviceType
from .forms import ConsumeEnergyForm, ProduceEnergyForm, StoreEnergyForm
from .models import ConsumeEnergyDevice, ProduceEnergyDevice, StoreEnergyDevice

dev_type_to_form = {
    DeviceType.CONSUME.value: ConsumeEnergyForm,
    DeviceType.STORE.value: StoreEnergyForm,
    DeviceType.PRODUCE.value: ProduceEnergyForm,
}

dev_type_to_model = {
    DeviceType.CONSUME.value: ConsumeEnergyDevice,
    DeviceType.STORE.value: StoreEnergyDevice,
    DeviceType.PRODUCE.value: ProduceEnergyDevice,
}

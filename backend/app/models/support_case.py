from pydantic import BaseModel


class SupportCase(BaseModel):
    customer_name: str
    phone_number: str
    country: str

    payment_verified: bool
    extension_triggered: bool
    api_success: bool
    skg_success: bool
    device_online: bool
    sim_slot_one: bool
    mobile_data_on: bool

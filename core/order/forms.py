from django import forms
from order.models import UserAddressModel,CouponModel
from django.utils import timezone

class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    coupon_code = forms.CharField(max_length=100, required=False)  # فیلد کوپن به صورت اختیاری

    

    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(CheckOutForm, self).__init__(*args, **kwargs)
        
    # def clean_address_id(self):
    #     address_id = self.cleaned_data.get('address_id')

    #     # Check if the address_id belongs to the requested user
    #     user = self.request.user  # Assuming the user is available in the request object
    #     try:
    #         address = UserAddressModel.objects.get(id=address_id, user=user)
    #     except UserAddressModel.DoesNotExist:
    #         raise forms.ValidationError("Invalid address for the requested user.")

    #     return address
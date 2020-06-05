

def create_or_update_user_profile(phone_number, address, pincode, delivery_slot):
    from core.models import User, UserProfile
    up = None
    try:
        up = UserProfile.objects.get(user_fk__phone_number=phone_number)
        up.address = address
        up.pincode = pincode
        up.delivery_slot = delivery_slot
        up.save()
    except Exception as e:
        u = User.objects.get(phone_number=phone_number)
        up = UserProfile.objects.create(user_fk=u, address=address, pincode=pincode, delivery_slot_pref=delivery_slot)
    return up

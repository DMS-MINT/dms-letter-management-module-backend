def user_profile_details(*, user_instance):
    user_profile = user_instance.user_profile.first()
    return {
        "id": user_instance.id,
        "first_name_en": user_profile.first_name_en if user_profile else None,
        "middle_name_en": user_profile.middle_name_en if user_profile else None,
        "last_name_en": user_profile.last_name_en if user_profile else None,
        "first_name_am": user_profile.first_name_am if user_profile else None,
        "middle_name_am": user_profile.middle_name_am if user_profile else None,
        "last_name_am": user_profile.last_name_am if user_profile else None,
        "full_name_en": user_profile.full_name_en if user_profile else None,
        "full_name_am": user_profile.full_name_am if user_profile else None,
        "job_title": {
            "title_en": user_profile.job_title.title_en if user_profile else None,
            "title_am": user_profile.job_title.title_am if user_profile else None,
        },
        "department": {
            "department_name_en": user_profile.department.department_name_en if user_profile else None,
            "department_name_am": user_profile.department.department_name_am if user_profile else None,
        },
        "email": user_instance.email,
        "phone_number": user_profile.phone_number if user_profile else None,
        "is_staff": user_instance.is_staff,
        "is_superuser": user_instance.is_superuser,
    }

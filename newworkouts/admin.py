from django.contrib import admin
from newworkouts.models import (Post_workout,
                                Rep_Configurations,
                                Set_Configurations,
                                Time_Configurations)


admin.ModelAdmin.list_per_page = 5000
admin.ModelAdmin.search_fields = ['title', 'purpose']
admin.site.register(Post_workout)
admin.site.register(Rep_Configurations)
admin.site.register(Set_Configurations)
admin.site.register(Time_Configurations)




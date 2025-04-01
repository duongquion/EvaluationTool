from django.contrib import admin
from .models import (
    Criteria, 
    CriteriaVersion, 
    InputType, 
    ResultPolicy, 
    VariableRelationship
)

class InputTypeAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'display_min', 'display_max')
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Limits', {'fields': ('min','max')})
    )
    search_fields = ('name',)
    ordering = ('name',)

    def display_min(self, obj):
        return '-∞' if obj.min is None else obj.min
    display_min.short_description = 'Min'

    def display_max(self, obj):
        return '+∞' if obj.max is None else obj.max
    display_max.short_description = 'Max'
        


class CriteriaVersionAdmin(admin.ModelAdmin):
    
    list_display = (
        'version_name', 
        'role_name', 
        'state', 
        'updated_at', 
        'updated_user'
    )
    fieldsets = (
        ('Create the version', {'fields': ('version_name',)}),
        ('Choose the role and state', {'fields': ('role_name','state')})
    )
    
    list_filter = ('role_name', 'state', )
    search_fields = ('version_name', 'role_name', )

class CriteriaAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "alias",
        "parent_alias",
        "version",
        "is_input",
        "input_type",
    )
    fieldsets = (
        ('Choose the version', {'fields': ('version',)}),
        ('Create data and function calculation', {'fields': ('name', 'alias','parent_alias', 'description', 'is_input', 'input_type','expression','is_final_result')})
    )

    list_filter = ('version','is_input', 'is_final_result')
    search_fields = ('version','name','input_type')

class ResultPolicyAdmin(admin.ModelAdmin):
    list_display = (
        'version', 
        'grading_rule', 
        'action_grades', 
        'explanation_grades',
    )

    fieldsets = (
        ('Choose the version', {'fields': ('version',)}),
        ('Add result policy', {'fields': ('grading_rule', 'action_grades', 'explanation_grades',)})
    )

    list_filter = ('version', )
    search_fields = ('version', )

class VariableRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        'version', 
        'from_alias', 
        'to_alias'
    )

    fieldsets = (
        ('Choose the version', {'fields': ('version',)}),
        ('Add variable relationship', {'fields': ('from_alias', 'to_alias', )})
    )

    list_filter = ('version', )
    search_fields = ('version', )

admin.site.register(InputType,InputTypeAdmin)
admin.site.register(CriteriaVersion,CriteriaVersionAdmin)
admin.site.register(Criteria,CriteriaAdmin)
admin.site.register(ResultPolicy, ResultPolicyAdmin)
admin.site.register(VariableRelationship, VariableRelationshipAdmin)
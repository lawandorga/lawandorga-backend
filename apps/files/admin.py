from apps.files.models import File, Folder, FolderPermission, PermissionForFolder
from django.contrib import admin


class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ('name', 'key', 'exists', 'created')

    def get_form(self, request, obj=None, **kwargs):
        form = super(FileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['key'].widget.attrs['style'] = 'width: 900px;'
        return form


class FolderAdmin(admin.ModelAdmin):
    model = Folder
    list_display = ('name', 'parent_name', 'same_parent', 'rlc')

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else ''

    @admin.display(boolean=True)
    def same_parent(self, obj):
        return obj == obj.parent


admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(FolderPermission)
admin.site.register(PermissionForFolder)

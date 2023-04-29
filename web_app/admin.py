from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse


class CustomSiteContentAdmin(admin.ModelAdmin):
    list_display = ["site_name","status","created_at","updated_at"]

class CustomPageContentAdmin(admin.ModelAdmin):
    search_fields = ["id","url"]
    list_display = ["url","page_url","status","created_at","updated_at"]
    list_filter = ["status"]
    ordering = ["-updated_at"]

    def page_url(self,obj):
        doctor_obj = Doctor.objects.all()
        service_obj = Service.objects.all()
        if obj.url == "/":
            url = "/"
        elif doctor_obj and obj.url == "doctors/{{x}}":
            url = reverse("web_app:doctor_url",args=[doctor_obj.first().slug])
        elif service_obj and obj.url == "services/{{x}}":
            url = reverse("web_app:services",args=[service_obj.first().slug])
        else:
            url = f"/{obj.url}/"
        return format_html(f"<a href='{url}' target='_blank'>{url}</a>")
    

    def save_model(self, request, obj, form, change):
        for cobj in CustomPageContent.objects.all():
            if obj.id != cobj.id:
                cobj.top_img = obj.top_img
                cobj.save()
        super().save_model(request, obj, form, change)
    

# class HomePageServicesInline(admin.StackedInline):
#     model = HomePageServices
#     extra = 0

class TESTIMONIALInline(admin.StackedInline):
    model = TESTIMONIAL
    extra = 0

class HomePageAdmin(admin.ModelAdmin):
    inlines = [TESTIMONIALInline]


admin.site.register(HomePage, HomePageAdmin)
admin.site.register(CustomSiteContent,CustomSiteContentAdmin)
admin.site.register(CustomPageContent,CustomPageContentAdmin)



######################################## Doctor Schema ########################################
class DoctorSocialLinksInline(admin.StackedInline):
    model = DoctorSocialLinks
    can_delete = True
    extra = 0
    max_num = 10

class DoctorAlumniInline(admin.StackedInline):
    model = DoctorAlumni
    can_delete = True
    extra = 0
    min_num = 1
    max_num = 10

class DoctorAwardInline(admin.StackedInline):
    model = DoctorAward
    can_delete = True
    extra = 0
    max_num = 10

class DoctorColleagueInline(admin.StackedInline):
    model = DoctorColleague
    can_delete = True
    extra = 0
    max_num = 10
    fk_name = "doctor"

class DoctorEducationalOccupationalCredentialInline(admin.StackedInline):
    model = DoctorEducationalOccupationalCredential
    can_delete = True
    extra = 0
    max_num = 10

class DoctorOccupationInline(admin.StackedInline):
    model = DoctorOccupation
    can_delete = True
    extra = 0
    min_num = 1
    max_num = 10

class DoctorExpertiseInline(admin.StackedInline):
    model = DoctorExpertise
    can_delete = True
    extra = 0
    min_num = 1
    max_num = 10

class DoctorKnowsLanguageInline(admin.StackedInline):
    model = DoctorKnowsLanguage
    can_delete = True
    extra = 0
    max_num = 10

class DoctorMemberOfOrganizationInline(admin.StackedInline):
    model = DoctorMemberOfOrganization
    can_delete = True
    extra = 0
    max_num = 10

class DoctorWorksForOrganizationInline(admin.StackedInline):
    model = DoctorWorksForOrganization
    can_delete = True
    extra = 0
    max_num = 10

class DoctorExtraInformationInline(admin.StackedInline):
    model = DoctorExtraInformation
    can_delete = True
    extra = 0
    max_num = 10


class DoctorAdmin(admin.ModelAdmin):
    inlines = [
        DoctorOccupationInline,
        DoctorAlumniInline,
        DoctorExpertiseInline,
        DoctorAwardInline,
        DoctorMemberOfOrganizationInline,
        DoctorWorksForOrganizationInline,
        DoctorKnowsLanguageInline,
        DoctorEducationalOccupationalCredentialInline,
        DoctorColleagueInline,
        DoctorSocialLinksInline,
        DoctorExtraInformationInline
    ]
    list_display = ["name","live_url","gender","honorific_prefix","honorific_suffix"]
    
    def live_url(self,obj):
        url = reverse("web_app:doctor_url",args=[obj.slug])
        return format_html(f"<a href='{url}' target='_blank'>{url}</a>")

admin.site.register(Doctor,DoctorAdmin)







######################################## Business Schema ########################################
# admin.site.register(Currency)
# admin.site.register(KnowsLanguage)


from django.forms import TextInput
class OpeningHoursInline(admin.TabularInline):
    insert_after = 'curreny_Accepted'
    model = OpeningHours
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'timing':
            kwargs['widget'] = TextInput(attrs={'size': '8'})
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class AdressInline(admin.StackedInline):
    insert_after = 'payment_Accepted'
    model = Adress
    extra = 0

class GeoInline(admin.StackedInline):
    insert_after = 'payment_Accepted'

    model = Geo
    extra = 0

class AreaServedInline(admin.StackedInline):
    insert_after = 'isAcceptingNewPatients'

    model = AreaServed
    extra = 0

class ContactPointInline(admin.StackedInline):
    insert_after = 'isAcceptingNewPatients'

    model = ContactPoint
    extra = 0


class ImageInline(admin.StackedInline):
    insert_after = 'knows_language'

    model = Image
    extra = 0


class HaspartInline(admin.StackedInline):
    insert_after = 'SameAs'

    model = Haspart
    extra = 0

class BusinessAdmin(admin.ModelAdmin):
    fields = ["type",'map_id','additional_Type','medical_Specialty','curreny_Accepted',"payment_Accepted","hasMap","logo","telephone","isAcceptingNewPatients","knows_language","url","name","AlternateName","description","disambiguatingDescription","foundingDate","SameAs"]

    inlines = [OpeningHoursInline,AdressInline,GeoInline,AreaServedInline,ContactPointInline,ImageInline,HaspartInline]

    change_form_template = 'admin/custom/change_form.html'
    class Media:
        css = {
            'all': (
                'css/admin.css',
            )
        }
   
admin.site.register(Business, BusinessAdmin)



class QuestionAdmin(admin.ModelAdmin):
    list_display = ["name","date"]
    readonly_fields = ("date",)


admin.site.register(Question,QuestionAdmin)




######################################## Service Schema ########################################

class HospitalAboutsInline(admin.TabularInline):
    model = ServiceAbout
    readonly_fields = ('id',)
    extra = 1

class HospitalmentionsInline(admin.TabularInline):
    model = ServiceMentions
    readonly_fields = ('id',)
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [HospitalAboutsInline, HospitalmentionsInline]
    list_display = ["name","live_url","type","reviewed_by"]
    
    def live_url(self,obj):
        url = reverse("web_app:services",args=[obj.slug])
        return format_html(f"<a href='{url}' target='_blank'>{url}</a>")




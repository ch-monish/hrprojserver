from django.urls import path

from pdf.views import PDFGeneration


urlpatterns = [
    # path('', views.PDF, name='PDF'),
    path('/jdpdf', PDFGeneration.as_view({'post': 'jdpdf'})),
    path('/offerletterpdf', PDFGeneration.as_view({'post': 'offerletterpdf'})),
    
]
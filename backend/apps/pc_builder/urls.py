from django.urls import path, include
from django.conf import settings
from apps.pc_builder.views import BuilderView

urlpatterns = [
    path('builder-list/', BuilderView.as_view(), name='builder-list'),

]

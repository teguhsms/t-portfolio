from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('portal.views',
    url(r'^$', 'main', name='main'),
    url(r'^login$', 'login', name='login'),
    url(r'^signin$', 'signin', name='signin'),
    url(r'^signup$', 'signup', name='signup'),


    #Admin Side
    url(r'^admin$','admin', name='admin'),
    url(r'^about$','about', name='about'),

    #Main
    url(r'^main_about','main_about', name='main_about'),

    url(r'^aboutAdmin$', 'aboutAdmin', name='aboutAdmin'),
    url(r'^adminpanel$', 'adminpanel', name='adminpanel'),
    url(r'^logout$', 'logout', name='logout'),
#    url(r'^dashboard$', 'dashboard', name='dashboard'),
    url(r'^index2$', 'index2', name='index2'),
    url(r'^lockme', 'lockme', name='lockme'),
    url(r'^iconPop$', 'iconPop', name='iconPop'),
    url(r'^lock_screen$', 'lock_screen', name='lock_screen'),
    #header
    url(r'^header$', 'header', name='header'),
    url(r'^logo$', 'logo', name='logo'),
    url(r'^skill$', 'skill', name='skill'),
    #button
    url(r'^icons$', 'icons', name='icons'),
    url(r'^services$', 'services', name='services'),
    url(r'^form$', 'form', name='form'),

)


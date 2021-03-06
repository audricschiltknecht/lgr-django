# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.utils import six
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from .utils import BaseDisableableFormSet

from .fields import UNICODE_VERSIONS, DEFAULT_UNICODE_VERSION, VALIDATING_REPERTOIRES, DEFAULT_VALIDATING_REPERTOIRE


def DateInputPlaceHolder(placeholder=''):
    """
     Return a DateInput form with 'datepicker' class
     and an optional place holder value.
    """
    return forms.DateInput({'class': 'datepicker',
                            'placeholder': placeholder})


def TextInputPlaceHolder(placeholder):
    """
     Return a TextInput form a place holder value.
    """
    return forms.TextInput(attrs={'placeholder': placeholder})

DESCRIPTION_CONTENT_TYPES = (
    ('', ''),
    ('text/plain', 'text/plain'),
    ('text/html', 'text/html'),
)


class MetadataForm(forms.Form):
    version = forms.CharField(label=_("Version"), max_length=255, required=False)
    version_comment = forms.CharField(label=_("Version comment"), required=False)
    date = forms.DateField(label=_("Date"), widget=DateInputPlaceHolder(date.today().isoformat()), required=False)
    scope = forms.CharField(label=_("Scope"), max_length=255, required=False, widget=TextInputPlaceHolder('example'))  # XXX: we may need to support multiple scope elements
    scope_type = forms.CharField(label=_("Scope type"), max_length=255, required=False, widget=TextInputPlaceHolder('domain'))
    validity_start = forms.DateField(label=_("Validity start"), widget=DateInputPlaceHolder(), required=False)
    validity_end = forms.DateField(label=_("Validity end"), widget=DateInputPlaceHolder(), required=False)
    unicode_version = forms.ChoiceField(label=_("Unicode version"), choices=UNICODE_VERSIONS, initial=DEFAULT_UNICODE_VERSION, required=False)
    description = forms.CharField(label=_("Description"), widget=forms.Textarea, required=False)
    description_type = forms.ChoiceField(label=_("Description type"), choices=DESCRIPTION_CONTENT_TYPES, required=False)

    validating_repertoire = forms.ChoiceField(label=_("Validating repertoire"),
                                              choices=(
                                                  ('', ''),
                                                  (_('Built-in'), VALIDATING_REPERTOIRES),
                                              ),
                                              initial=DEFAULT_VALIDATING_REPERTOIRE,
                                              required=False)

    def __init__(self, *args, **kwargs):
        additional_repertoires = kwargs.pop('additional_repertoires', [])
        disabled = kwargs.pop('disabled')
        super(MetadataForm, self).__init__(*args, **kwargs)
        if additional_repertoires:
            # dynamically append the session LGRs (by copy, not by reference)
            self.fields['validating_repertoire'].choices = self.fields['validating_repertoire'].choices + [
                (_('My LGRs'), tuple((rname, rname) for rname in additional_repertoires))]
        if disabled:
            # do not enable to update references for LGRs in a set
            for field in six.itervalues(self.fields):
                # field.disabled = True  XXX need django 1.9
                field.widget.attrs['disabled'] = True


class LanguageForm(forms.Form):
    # validate using language_tags function
    language = forms.CharField(label=_("Language"), max_length=50, required=False)  # https://tools.ietf.org/html/rfc5646#section-4.4


LanguageFormSet = formset_factory(LanguageForm,
                                  formset=BaseDisableableFormSet,
                                  extra=1)

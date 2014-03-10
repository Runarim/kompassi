# encoding: utf-8

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden

from core.utils import DateField

from .models import Person, EMAIL_LENGTH, PHONE_NUMBER_LENGTH, BIRTH_DATE_HELP_TEXT
from .utils import horizontal_form_helper, indented_without_label, check_password_strength


valid_username = RegexValidator(
    regex=r'[a-z0-9_]{4,30}',
    message=u'Käyttäjänimi ei kelpaa.'
)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=30, label=u'Käyttäjänimi')

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana',
        widget=forms.PasswordInput,
    )

    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            'next',
            Fieldset(u'Kirjaudu sisään {}'.format(settings.TURSKA_ACCOUNT_BRANDING_2ND_PERSON_ADESSIVE),
                'username',
                'password',
                indented_without_label(Submit('submit', u'Kirjaudu sisään', css_class='btn-primary'), css_class='col-md-offset-4 col-md-8')
            )
        )


class PersonForm(forms.ModelForm):
    birth_date = DateField(required=True, label=u'Syntymäaika', help_text=BIRTH_DATE_HELP_TEXT)
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH, label=u'Sähköpostiosoite')
    phone = forms.CharField(required=True, max_length=PHONE_NUMBER_LENGTH, label=u'Puhelinnumero')

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

        if self.instance.pk is None:
            save_button_text = u'Rekisteröidy'
        else:
            save_button_text = u'Tallenna tiedot'

        self.helper.layout = Layout(
            Fieldset(u'Perustiedot',
                'first_name',
                'surname',
                'nick',
                'birth_date'
            ),
            Fieldset(u'Yhteystiedot',
                'phone',
                'email',
                indented_without_label('may_send_info'),
            ),
            indented_without_label(Submit('submit', save_button_text, css_class='btn-primary'))
        )

    class Meta:
        model = Person
        fields = (
            'may_send_info',
            'first_name',
            'surname',
            'nick',
            'birth_date',
            'email',
            'phone',
        )


PASSWORD_HELP_TEXT = (
    u'Salasanan tulee olla vähintään {min_length} merkkiä pitkä ja sisältää ainakin '
    u'{min_classes} seuraavista: pieni kirjain, iso kirjain, numero, erikoismerkki.'
    .format(
        min_classes=settings.TURSKA_PASSWORD_MIN_CLASSES,
        min_length=settings.TURSKA_PASSWORD_MIN_LENGTH,
    )
)


class RegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=30,
        validators=[valid_username],
        label=u'Käyttäjänimi',
        help_text=u'Valitse itsellesi 4&ndash;30 merkin pituinen käyttäjänimi. Sallittuja '
            u'merkkejä ovat kirjaimet <i>a&ndash;z</i>, numerot <i>0&ndash;9</i> sekä '
            u'alaviiva </i>_</i>.'
    )

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana',
        widget=forms.PasswordInput,
        validators=[check_password_strength],
    )
    password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana uudestaan',
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    accept_terms_and_conditions = forms.BooleanField(
        required=True,
        label=u'Annan luvan henkilötietojeni käsittelyyn <a href="{}" target="_blank">rekisteriselosteen</a> mukaisesti <i>(pakollinen)</i>'.format(settings.TURSKA_PRIVACY_POLICY_URL)
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Käyttäjätunnus ja salasana',
                'username',
                'password',
                'password_again'
            ),
            Fieldset(u'Suostumus henkilötietojen käsittelyyn',
                indented_without_label('accept_terms_and_conditions')
            ),
        )

    def clean_username(self):
        from django.contrib.auth.models import User

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Käyttäjänimi on jo käytössä.')

        return username

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            raise forms.ValidationError(u'Salasanat eivät täsmää.')

        return password_again


class PasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Vanha salasana',
        widget=forms.PasswordInput,
    )

    new_password = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Uusi salasana',
        widget=forms.PasswordInput,
        validators=[check_password_strength],
    )

    new_password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana uudestaan',
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('the_request')

        super(PasswordForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            Fieldset(u'Salasanan vaihto',
                'old_password',
                'new_password',
                'new_password_again',
            ),
            indented_without_label(Submit('submit', "Vaihda salasana", css_class='btn-primary'))
        )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        authenticated_user = authenticate(
            username=self.request.user.username,
            password=old_password
        )

        if not authenticated_user:
            raise forms.ValidationError(u'Vanha salasana on väärä.')

        return old_password

    def clean_new_password_again(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_again = self.cleaned_data.get('new_password_again')

        if new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError(u'Salasanat eivät täsmää.')

        return new_password_again


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH, label=u'Sähköpostiosoite')

    def __init__(self, *args, **kwargs):
        super(PasswordResetRequestForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'email',
            indented_without_label(Submit('submit', u'Lähetä', css_class='btn-success'))
        )

class PasswordResetForm(forms.Form):
    # XXX BEGIN UGLY COPYPASTA
    new_password = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Uusi salasana',
        widget=forms.PasswordInput,
        validators=[check_password_strength],
    )

    new_password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana uudestaan',
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def clean_new_password_again(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_again = self.cleaned_data.get('new_password_again')

        if new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError(u'Salasanat eivät täsmää.')

        return new_password_again
    # XXX END UGLY COPYPASTA

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'new_password',
            'new_password_again',
            indented_without_label(Submit('submit', u'Vaihda salasana', css_class='btn-success'))
        )

import re
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Regexp
from wtforms import (
    URLField, DateField, SelectField,
    TimeField, StringField, BooleanField,
    TextAreaField, SubmitField, Field
)
from wtforms.widgets import TextInput

re_duracao = re.compile(r"^(?:(?P<hora>[0-5]?[0-9]):)?(?:(?P<minuto>[0-5]?[0-9])?:)?(?P<segundo>[0-5]?[0-9])?$")

VALOR_OUTROS = '-'
VALOR_NULO = '_nulo'


class DurationField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            s = self.data.seconds % 60
            m = (self.data.seconds // 60) % 60
            h = self.data.seconds // 3600
            return f'{h:02d}:{m:02d}:{s:02d}'
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            match = re_duracao.match(valuelist[0])
            if match is not None:
                segundo = match['segundo']
                minuto = match['minuto']
                hora = match['hora']

                self.data = timedelta(
                    seconds=int(segundo) if segundo is not None else 0,
                    minutes=int(minuto) if minuto is not None else 0,
                    hours=int(hora) if hora is not None else 0
                )
            else:
                print(f"invalid data: {valuelist[0]}")
                self.data = VALOR_NULO
        else:
            self.data = VALOR_NULO    # noqa


class Formulario(FlaskForm):
    url = URLField('url', validators=[DataRequired()])

    data = DateField('data', validators=[DataRequired()])

    turno = SelectField(
        'turno',
        validators=[DataRequired()],
        choices=[
            ('M', 'Manhã'), ('M1', 'Manhã 1'), ('M2', "Manhã 2"),
            ('T', 'Tarde'), ('T1', 'Tarde 1'), ('T2', "Tarde 2"),
            ('N', 'Noite'), ('N1', 'Noite 1'), ('N2', "Noite 2"),
            (VALOR_OUTROS, 'Outro')
        ]
    )
    turno_alt = StringField('turnoAlt')

    titulo = StringField('titulo', validators=[DataRequired()])

    pregador = SelectField(
        'pregador',
        validators=[DataRequired()],
        choices=[('-', 'Outro')]
    )
    pregador_alt = StringField('pregadorAlt')

    serie = SelectField(
        'serie',
        validators=[DataRequired()],
        choices=[(VALOR_OUTROS, 'Outro'), (VALOR_NULO, '(Sem Série)')]
    )
    serie_alt = StringField('serieAlt')

    # inicio = DurationField('inicio')
    inicio = StringField('inicio', validators=[Regexp(re_duracao)])
    fade_in = BooleanField('fadeIn')

    fim = StringField('fim', validators=[Regexp(re_duracao)])
    fade_out = BooleanField('fadeOut')

    comentario = TextAreaField('comentario')

    submit = SubmitField('submit')

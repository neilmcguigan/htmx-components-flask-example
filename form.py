from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DateTimeLocalField,
    DecimalField,
    DecimalRangeField,
    EmailField,
    FileField,
    FloatField,
    HiddenField,
    IntegerField,
    IntegerRangeField,
    MonthField,
    MultipleFileField,
    PasswordField,
    RadioField,
    SearchField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TelField,
    TextAreaField,
    TimeField,
    URLField,
    validators,
)
from wtforms.widgets import ColorInput, PasswordInput, WeekInput


class ColorField(StringField):
    widget = ColorInput()


req = validators.InputRequired()
desc = "A description"


class KitchenSink(FlaskForm):
    string = StringField("String", description=desc, validators=[req])
    search = SearchField("Search", description=desc, validators=[req])
    password = PasswordField(
        "Password",
        widget=PasswordInput(hide_value=False),
        description=desc,
        validators=[req],
    )
    email = EmailField("Email", description=desc, validators=[req, validators.Email()])
    tel = TelField("Tel", description=desc, validators=[req])
    url = URLField("URL", description=desc, validators=[req, validators.URL()])
    textarea = TextAreaField("Text Area", description=desc, validators=[req])

    boolean = BooleanField("Checkbox", description=desc, validators=[req])

    choices = [("a", "A"), ("b", "B"), ("c", "C")]
    radio = RadioField(
        "Radio",
        choices=choices,
        description=desc,
        validators=[validators.DataRequired()],
    )
    select = SelectField(
        label="Select",
        description=desc,
        choices=[("", "-- Select --")] + choices,
        validators=[req],
    )
    multiselect = SelectMultipleField(
        label="Select Multiple", description=desc, choices=choices, validators=[req]
    )

    date = DateField("Date", description=desc, validators=[req])

    datetimelocal = DateTimeLocalField(
        "DateTime Local",
        description=desc,
        format="%Y-%m-%dT%H:%M",
        validators=[req],
    )
    week = DateField(
        "Week",
        widget=WeekInput(),
        description=desc,
        validators=[req],
        format="%Y-W%U",
    )
    month = MonthField("Month", description=desc, validators=[req])
    time = TimeField("Time", description=desc, validators=[req])

    integer = IntegerField("Integer", description=desc, validators=[req])
    decimal = DecimalField("Decimal", description=desc, validators=[req])
    float = FloatField("Float", description=desc, validators=[req])
    integerrange = IntegerRangeField(
        "Integer Range",
        description=desc,
        render_kw={"min": 0, "max": 100},
        validators=[validators.NumberRange(min=51)],
    )
    decimalrange = DecimalRangeField(
        "Decimal Range",
        description=desc,
        render_kw={"min": 0, "max": 100},
        validators=[validators.NumberRange(min=51)],
    )

    file = FileField(
        "File",
        # validators=[FileRequired()],
        description=desc,
    )
    multifile = MultipleFileField(
        "Multi-File",
        # validators=[FileRequired()],
        description=desc,
    )
    color = ColorField("Color", description=desc)

    hidden = HiddenField("", default="I'm hidden")
    submit = SubmitField("Submit")

from marshmallow import Schema, fields

class Evaluacion(Schema):
    id = fields.Integer()
    uid = fields.Integer()
    date = fields.Str()
    peso = fields.Number()
    estatura = fields.Number()
    imc = fields.Number()
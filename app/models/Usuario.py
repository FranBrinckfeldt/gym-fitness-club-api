from marshmallow import Schema, fields

class Usuario(Schema):
    id = fields.Integer()
    usuario = fields.Str()
    nombre = fields.Str()
    apellido = fields.Str()
    fechaNacimiento = fields.Str()
    clave = fields.Str()
    estatura = fields.Decimal()
from abc import ABC

class Field(ABC):
    def __init__(self, field_type, max_length=None, unique=False, nullable=True):
        self.field_type = field_type
        self.max_length = max_length
        self.unique = unique
        self.nullable = nullable

    def to_sql(self):
        sql = [self.field_type]

        if self.field_type == 'VARCHAR' and self.max_length:
            sql[0] = f'VARCHAR({self.max_length})'
        if self.unique:
            sql.append('UNIQUE')
        if not self.nullable:
            sql.append('NOT NULL')

        return ' '.join(sql)

class CharField(Field):
    def __init__(self, max_length=255, unique=False, nullable=True):
        super().__init__('VARCHAR', max_length, unique, nullable)

class IntegerField(Field):
    def __init__(self, unique=False, nullable=True):
        super().__init__('INTEGER', None, unique, nullable)

class ForeignKeyField(Field):
    def __init__(self, to_model, unique=False, nullable=False):
        self.to_model = to_model
        super().__init__('INTEGER', None, unique, nullable)

    def get_constraint(self, name):
        table_name = self.to_model.__name__.lower()
        return f"FOREIGN KEY ({name}) REFERENCES {table_name}(id)"
class Model:
    db = None
    connection = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def _get_table_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_fields(cls):
        from DB_and_Related.fields import Field
        return {key: value for key, value in cls.__dict__.items() if isinstance(value, Field)}

    @classmethod
    def get_table_constraints(cls):
        return []

    @classmethod
    def create_table(cls):
        if not cls.connection:
            return

        fields = cls.get_fields()
        columns_sql = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        constraints = []

        for name, field in fields.items():
            columns_sql.append(f"{name} {field.to_sql()}")
            if hasattr(field, 'get_constraint'):
                constraints.append(field.get_constraint(name))

        table_constraints = cls.get_table_constraints()

        all_sql = columns_sql + constraints + table_constraints
        query = f"CREATE TABLE IF NOT EXISTS {cls._get_table_name()} ({', '.join(all_sql)})"

        cls.connection.execute(query)
        cls.connection.commit()
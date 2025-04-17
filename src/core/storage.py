import lancedb

# Database storage class
class Storage:
    def __init__(self, uri, table, schema):
        self.uri = uri
        self.table_name = table
        self.schema = schema
        self.db = lancedb.connect(uri=self.uri)

        # Initialize the table
        if self.table_name not in self.db.table_names():
            self.table = self.db.create_table(self.table_name, schema=schema)
        else:
            self.table = self.db.open_table(self.table_name)
            schema_fields = [field.name for field in self.table.schema]
            if schema_fields != list(self.schema.model_fields.keys()):
                raise RuntimeError(f"Table {self.table_name} has a different schema.")
            
        
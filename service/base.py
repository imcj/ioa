from aiomysql.sa.engine import _EngineContextManager

class Service:
    engine : _EngineContextManager = None
    
    def __init__(self, engine):
        self.engine = engine

    def row2dict(self, row):
        if not row:
            return None
        d = {}
        for column in row.keys():
            d[column] = row[column]

        return d
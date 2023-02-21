

class Querys_Advance:

    def __init__(self, bd):
        self.bd = bd


    def Check_Exist_Content(self, table, consult_atribute, id_atribute ) -> bool:
        querys = """
        SELECT
            CASE 
                WHEN COUNT({}) > 0 then 1 else 0
                END as cant
        from {}
        WHERE {} = {}
        """.format(consult_atribute, table, consult_atribute, id_atribute)
        return bool(self.bd.consultar(querys)["datos"][0])

import cx_Oracle
import mybatis_mapper2sql
import xml.etree.ElementTree as elemTree

keyXml = elemTree.parse('../keys.xml')
db_address = keyXml.find('string[@name="db_address"]').text

class DaoScrap:
    def __init__(self):
        self.conn = cx_Oracle.connect(db_address)
        self.cs = self.conn.cursor()
        self.mapper = mybatis_mapper2sql.create_mapper(xml='mapper/mybatis_scrap.xml')[0]
 
    def select_mine(self, mem_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "select_mine")
        rs = self.cs.execute(sql,(mem_id,))
        list = []
        for record in rs:
            list.append({'scrap_seq':record[0],'scrap_name':record[1],'scrap_comp':record[2],'scrap_url':record[3],'in_user_id':record[4]})
        return list
            
    def dupl_mine(self, scrap_name, mem_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "dupl_mine")
        rs = self.cs.execute(sql, (scrap_name, mem_id))
        list = []
        for record in rs:
            list.append({'scrap_name':record[0],'in_user_id':record[1]})
        return list

    def insert(self, scrap_name, scrap_comp, scrap_url, mem_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "insert")
        self.cs.execute(sql, (scrap_name, scrap_comp, scrap_url, mem_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt

    def delete(self, scrap_seq, mem_id):
        sql = mybatis_mapper2sql.get_child_statement(self.mapper, "delete")  
        self.cs.execute(sql, (scrap_seq, mem_id))
        self.conn.commit()
        cnt = self.cs.rowcount
        return cnt
        
    def __del__(self): 
        self.cs.close()
        self.conn.close()
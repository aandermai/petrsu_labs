from neo4j import GraphDatabase

URI = "bolt://44.211.218.63:7687"
AUTH = ("neo4j", "chatter-intercom-pear")

driver = GraphDatabase.driver(URI, auth=AUTH)

try:
    driver.verify_connectivity()
    print("✅ Подключение к Neo4j Aura установлено!")
except Exception as e:
    print(f"Ошибка подключения к БД: {e}")

query = """ 
MERGE (u:Person {name: "Жопа"})
"""

session = driver.session()

result = session.run(query)
print(list(result))

query = """
MATCH (p:Person)
WHERE p.name = "Жопа"  
RETURN p"""
result = session.run(query)
print(list(result))

session.close()
driver.close()
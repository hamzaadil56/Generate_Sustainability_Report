from langchain_community.document_loaders.sql_database import SQLDatabaseLoader
from langchain_community.document_loaders.sql_database import SQLDatabase
import getpass
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain


load_dotenv()

llm = ChatGroq(model="llama3-8b-8192")

db = SQLDatabase.from_uri(
    "postgresql://postgres:Hamza@localhost:5432/postgres")

execute_query = QuerySQLDataBaseTool(db=db)
# runn = queryTool.run("Bring all the tables from the database")
write_query = create_sql_query_chain(llm, db)

chain = write_query | execute_query
response = chain.invoke({"question": "How many companies are there?"})
print(response, 'response')

# print(db.run(response))
# toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# print(toolkit.get_tools())
# def test_run():
#     """Test with parametrization."""
#     loader = SQLDatabaseLoader("select * from companyinfo", db)
#     data = loader.load_and_split()

#     print(data)


# test_run()

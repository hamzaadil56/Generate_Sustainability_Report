from langchain_community.document_loaders.sql_database import SQLDatabase
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class SQLQuerySystem:
    def __init__(self, db_uri, model="llama-3.1-70b-versatile", top_k=5):
        load_dotenv()
        self.llm = ChatGroq(model=model)
        self.db = SQLDatabase.from_uri(db_uri)
        self.top_k = top_k
        self.setup_chain()

    def setup_chain(self):
        self.write_query_prompt = self.create_write_query_prompt()
        self.execute_query = QuerySQLDataBaseTool(db=self.db)
        self.write_query = create_sql_query_chain(
            self.llm, self.db, prompt=self.write_query_prompt)
        self.answer_prompt = self.create_answer_prompt()
        self.chain = self.create_chain()

    def create_write_query_prompt(self):
        template = """You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.
        Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per PostgreSQL. You can order the results to return the most informative data in the database.
        Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
        Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
        Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".

        Use the following format:

        Question: Question here
        SQLQuery: SQL Query to run
        SQLResult: Result of the SQLQuery
        Answer: Final answer here

        Only use the following tables:
        {table_info}

        Question: {input}

        Only Return SQL Query, no other text."""
        return PromptTemplate(
            template=template,
            input_variables=["table_info", "input", "top_k"],
        )

    def create_answer_prompt(self):
        return PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
            Your answer should be in the follwing json format. If something goes wrong with finding the data, just say "Can't able to find data'.

            {{
                "answer":string,
                "data_type":string,
                "chart_type":string,               
                data:[{{
                "company":string,
                "value":float,
                "year":int,
                }}]
            }}

            In the above json format, the data type can be either "text" or "data". If the the data type will be "text", then the "data" property will be null. And if the data type will be "data", then the "data" property will be in array format. And then a chart type should also be suggested from the following three types: 
              1) Bar
              2) Line
              3) Pie .       
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """


        )

    def create_chain(self):
        return (
            RunnablePassthrough.assign(query=self.write_query).assign(
                result=itemgetter("query") | self.execute_query
            )
            | self.answer_prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, question):
        return self.chain.invoke({
            "question": question
        })

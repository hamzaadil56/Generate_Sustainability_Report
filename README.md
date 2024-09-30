## 🌍 Inspiration
Large organizations and corporate companies are striving to increase sustainability globally. Gen AI has numerous use cases in sustainability development, one of which is **Sustainability Reporting and Boosting Collaboration** within companies. To enhance communication and reporting for sustainability, we developed **Sustainability Analytics**.

---

## 💡 What it Does
**Sustainability Analytics** provides an intelligent chatbot interface that allows users to ask real-time questions about a company’s sustainability data.

Key Features:
- Leverages ESG data and advanced AI models (like LLaMA 3.1) to retrieve accurate and relevant information.
- Users can inquire about:
  - Carbon emissions
  - Energy usage
  - Water consumption
  - And more!
- The chatbot generates:
  - **Year-on-year comparisons** 
  - **Visual insights** in the form of bar, line, and pie charts.

### Example:
**User Query:** "What are the total carbon emissions in 2024 for the respective company?"  
**Chatbot Response:** "The total carbon emissions for 2024 are **X metric tons**."

---

## 🛠️ How We Built It
**Tech Stack:**
- **Advanced RAG methodology** using the open-source **LLaMA 3.1** model.
- **Langchain framework** for querying data.
- **Postgres database** to store ESG metrics.
- **Backend:** Python framework **FastAPI**.
- **Frontend:** Built using **React.js**.

Data is queried through Langchain tools, which the **LLM** processes to generate natural language responses, along with chart visualizations.

---

## 🚧 Challenges We Ran Into
We encountered several challenges during development:

1. **Prompt Engineering:**
   - Ensuring the LLaMA 3.1 model accurately handles sustainability-related queries.
   
2. **Data Sourcing & Integration:**
   - Structuring ESG metrics data for easy querying through the Langchain framework.
   
3. **Performance Optimization:**
   - Enhancing the RAG methodology for large datasets and managing chart generation (bar, line, pie) for data comparisons.
   
4. **Accuracy Across Queries:**
   - Ensuring accuracy in dynamic year-on-year comparisons across diverse query types.

---

## 🏆 Accomplishments We're Proud Of
- **Successful Integration:** We integrated LLaMA 3.1 with Langchain to build an interactive sustainability analytics platform.
- **Real-Time Responses:** Our chatbot delivers accurate, context-specific answers about a company’s ESG metrics in real-time.
- **Dynamic Visualizations:** Users can generate visual insights (bar, line, pie charts) based on queries.
- **Efficient Querying:** Built a highly efficient querying mechanism for our Postgres database, ensuring speed without compromising accuracy.

---

## 🎓 What We Learned
- Mastering **advanced RAG methodology** helped us streamline the generation of precise responses.
- We learned to handle **ESG data** more effectively while building scalable backend systems that support data-heavy operations.
- Integrating databases with generative models taught us the importance of **data integrity** and query optimization.

---

## 🚀 What’s Next for Sustainability Analytics
We aim to expand **Sustainability Analytics** with:

1. **Advanced Data Analytics Features:**
   - Predictive analysis for forecasting future ESG metrics.
   - Identifying areas for sustainability improvement.
   
2. **Global Standards Integration:**
   - Adding more sustainability frameworks to align with global standards.
   - Support for multilingual capabilities for a broader client base.

3. **Collaboration Tools:**
   - Introducing tools that allow company stakeholders to collaboratively input data and generate comprehensive reports.

4. **API Integration:**
   - Expanding API integrations with existing sustainability platforms.
   
5. **User Interface Improvements:**
   - Enhancing the UI for a more intuitive user experience.

---

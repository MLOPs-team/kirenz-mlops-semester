#!/usr/bin/env python
# coding: utf-8

# # Notes: Required questions - theory Kirenz
# 

# ## Data-centric AI
# 
# Notes on the video of AI pioneer Andrew Ng:"A Chat with Andrew on MLOps: From Model-centric to Data-centric AI".
# 
# <iframe width="560" height="315" src="https://www.youtube.com/embed/06-AZXmwHjo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
# 
# 
# - **AI-System** = Code (model/algorithm) + Data 
# 
# - Data is food for AI  
# ![image](../../../assets/img/dataIsFood.png)     
# 
# - It's very important especially for small data sets that the labels are consistencly  
# ![image](../../../assets/img/smallDataAndLabelConsistency.png)  
# 
#     - **Noisy Dataset**: data that contains a large amount of additional meaningless information. E.g. corrupted data...all data that cannot be understood and interpreted  by a user system.
#     
#     - **Noisy labels**: labels that were set incorrectly or inconsitently  
# 
# 
# - **Theory: Clean vs. noisy Data**  
#     You have 500 Examples and 12% of the examples are noisy (incorrectly or inconsitently labeld)
# 
#     The following are about equally effective: 
#         - Clean up the noise => 60 examples
#         - Collect annother 500 new examples (double the training set)
#     
#     With a data centric view, there is significant of room for improvment in problems <10.000 examples
# 
# ```{admonition} Required questions
# :class: tip
# - **Describe the lifecycle of an ML project**
# 
# ____________________________
# 
# - **What is the difference between a model-centric vs data-centric view**  
#   
#     **Model-centric view**  
#     Collect what data you can, and develop a model good enough to deal with the noise in the data.  
# 
#     Hold the data fixed and iteratively improve the code/model.  
#       
#     **Data-centric view**  
#     The consistency of the data is paramount. Use tools to improve the data quality; this will allow multiple models to do well.  
# 
#     Hold the code fixed and iteratively improve the data..  
# ____________________________
# 
# - **Describe MLOps’ most important task**  
#   
#     Ensure consistently high-quality data in all phases oft he ML project lifecycle        
#     What is good Data?
#     - Defined consistently (definition of labels y is unambiguous)
#     - Cover of important cases (good coverage of inputs x)
#     - Enough data – for example enough data of speech with car noise in background
#     - Has timely feedback from production data (distribution covers data drift and concept drift)
#     - Sized appropriately
# 
# ```

# ## Common MLOps related challenges
# 
# Notes on the video of Nayur Khan, global head of technical delivery at McKinsey
# 
# <iframe width="560" height="315" src="https://www.youtube.com/embed/M1F0FDJGu0Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
# 
# ```{admonition} Required questions
# :class: tip
# - **Describe 4 typical challenges when creating machine learning products.**  
#     
#     What we typically find is that a couple of teams sitting in the same ofice or somethines geographically separateda and many problems result….  
#     
#     - *Lack of collaboration* or sharing of components/libaries betwenn the teams but even within the same team. 
#     - *Inconsistency*: Different approachtes to solving same problem, or using inonsistent data or algortihms
#     - *Duplicaton*: reinveting the wheel. Teams sitting next to each other and try to solve the same problem. 
#     - *Tech Debt*: Large codebases and tech debt. you don't know how to maintain your code
# 
# 
# ____________________________
# 
# - **Reusability concerns within a codebase: Explain a common way to look at what code is doing in a typical ML project.**  
#   
# ____________________________
# 
# - **What kind of problems does the open-source framework Kedro solve and where does Kedro fit in the MLOps ecosystem?**  
#   
#     Kedro solved to problem of maintability.   
# 
#     Kedro is not for the deployment. Kedro focuses on how you work while writing standardized, modular, maintabile and reproducible data sience code an does not focus on how you would like to run it in production. The responsibility of „What time will this pipeline run? And How will i know i fit failed? Is left to tools called orchestrators like Apache Airflow, Luigi, Dagster and Perfect. Orchestrators do not focus on the process of producing something that could be deployed, which is what Kedro does. 
# 
# 
# ```
# 
# 

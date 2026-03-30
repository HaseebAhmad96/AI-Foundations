LangChain: Chains & Runnables

Task: 
● Modular News Briefing Builder: Build a pipeline using only the official Runnable 
classes. A RunnableParallel fetches a headline summary and a sentiment score for 
a given topic at the same time. A RunnableLambda merges and formats the two 
results. A RunnableGenerator streams the final briefing sentence by sentence to the 
terminal. The full chain is composed with RunnableSequence via the | operator and 
called with a RunnableConfig that attaches a custom tag and callback for logging 
every step — all credentials in .env.
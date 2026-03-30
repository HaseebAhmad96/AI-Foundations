LangChain: Chains & Runnables

Task: 
● Research Report Generator: Build an LCEL chain that takes a raw topic, runs a 
key-facts prompt and a counterarguments prompt in parallel via RunnableParallel, 
merges both outputs using RunnableLambda, then passes the combined result into a 
final prompt that writes a balanced, structured research report saved to a .txt file.
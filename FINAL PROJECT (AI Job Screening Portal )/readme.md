Final Project — AI Job Screening Portal (Terminal Based)
 
The HR department needs a terminal application to screen job applicants end to end. It must 
accept raw CV files from a designated input folder, query multiple LLM providers to extract and 
validate structured candidate profiles using Pydantic models, rank applicants against a provided 
job description file using prompt chaining, and generate a timestamped shortlist report — all AI 
calls routed through a safety check, all activity logged cleanly to a file, and all credentials 
secured in a .env config.
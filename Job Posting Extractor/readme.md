LangChain: Structured Outputs & Output Parsers

Task: 
● Job Posting Extractor: Build a pipeline that takes raw job description text files. Define 
the extraction schema as a Pydantic model (job title, company, required skills list, 
experience level, salary range, remote status) with @field_validator ensuring 
experience level matches a Literal of fixed values and salary is a positive number. 
Use a PydanticOutputParser with .get_format_instructions() injected into 
the prompt, extract a structured record from each file, run malformed outputs through an 
OutputFixingParser, and save all validated results into a single clean JSON file 
using model_dump_json(). 
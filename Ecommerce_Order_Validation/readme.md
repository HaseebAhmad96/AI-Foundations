Pydantic

Task: 
● E-Commerce Order Validator: Build a terminal data validation system for an 
e-commerce platform. Define Pydantic models for Customer, Product, OrderItem, 
and Order with full constraints — prices must be positive, quantity at least 1, email must 
match a pattern, and status must be a Literal of allowed values. Use 
@field_validator to normalise all strings to title case, @model_validator to verify 
the order total matches the sum of all line items, and @computed_field to expose a 
total_with_tax field. Load a raw JSON file of orders, validate each with 
model_validate(), collect all validation errors without crashing, and write a clean 
validated orders file using model_dump_json() alongside a separate error report. 
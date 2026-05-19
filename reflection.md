## Week 3 Reflection

1. What was the most confusing thing about Python compared to JavaScript?

One confusing thing about Python compared to JavaScript was the indentation. In Python, indentation is very important because it defines blocks of code, while JavaScript uses curly braces. I also noticed Python syntax is simpler and cleaner in many cases.

2. What does an HTTP status code tell you? Give one example.

An HTTP status code tells you whether a request was successful or if there was an error. For example, status code 201 means a resource was successfully created, such as when adding a new book using POST /books.

3. What was the difference between a path parameter and a query parameter?

A path parameter is part of the URL path and identifies a specific resource, like /books/1. A query parameter is optional and used for filtering or searching, like /books?status=reading.

4. What would happen to all the data if you restarted the server right now? Why is that a problem, and what will we use to fix it?

If the server restarts, all the book data will disappear because the app currently uses in-memory storage. This is a problem because data is not permanent. In the future, we will use a real database to store data persistently.
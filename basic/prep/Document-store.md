
#### Document store

> Abstraction: key-value store with documents stored as values

A document store is centered around documents (XML, JSON, binary, etc), where a document stores all information for a given object. Document stores provide APIs or a query language to query based on the internal structure of the document itself. _Note, many key-value stores include features for working with a value's metadata, blurring the lines between these two storage types._

Based on the underlying implementation, documents are organized by collections, tags, metadata, or directories. Although documents can be organized or grouped together, documents may have fields that are completely different from each other.

Some document stores like [[mongodb architecture]] and [[]] also provide a SQL-like language to perform complex queries. [[decandia07dynamo]] supports both key-values and documents.

Document stores provide high flexibility and are often used for working with occasionally changing data.
##### Source(s) and further reading: document store
- [[Document oriented_database]]
- [[mongodb architecture]]
- [[]]
- [[found elasticsearch from the bottom up]]
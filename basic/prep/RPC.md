### Remote procedure call (RPC)

[[iF4Mkb5]]](https://github.com/donnemartin/system-design-primer/blob/master/images/iF4Mkb5.png)  
_[[2016 02 13 crack the system design interview]]_

In an RPC, a client causes a procedure to execute on a different address space, usually a remote server. The procedure is coded as if it were a local procedure call, abstracting away the details of how to communicate with the server from the client program. Remote calls are usually slower and less reliable than local calls so it is helpful to distinguish RPC calls from local calls. Popular RPC frameworks include [[]], [[]], and [[]].

RPC is a request-response protocol:

- **Client program** - Calls the client stub procedure. The parameters are pushed onto the stack like a local procedure call.
- **Client stub procedure** - Marshals (packs) procedure id and arguments into a request message.
- **Client communication module** - OS sends the message from the client to the server.
- **Server communication module** - OS passes the incoming packets to the server stub procedure.
- **Server stub procedure** - Unmarshalls the results, calls the server procedure matching the procedure id and passes the given arguments.
- The server response repeats the steps above in reverse order.

Sample RPC calls:

```
GET /someoperation?data=anId

POST /anotheroperation
{
  "data":"anId";
  "anotherdata": "another value"
}
```

RPC is focused on exposing behaviors. RPCs are often used for performance reasons with internal communications, as you can hand-craft native calls to better fit your use cases.

Choose a native library (aka SDK) when:

- You know your target platform.
- You want to control how your "logic" is accessed.
- You want to control how error control happens off your library.
- Performance and end user experience is your primary concern.

HTTP APIs following **REST** tend to be used more often for public APIs.

#### Disadvantage(s): RPC
- RPC clients become tightly coupled to the service implementation.
- A new API must be defined for every new operation or use case.
- It can be difficult to debug RPC.
- You might not be able to leverage existing technologies out of the box. For example, it might require additional effort to ensure [[]] on caching servers such as [[]].

### Representational state transfer (REST)
REST is an architectural style enforcing a client/server model where the client acts on a set of resources managed by the server. The server provides a representation of resources and actions that can either manipulate or get a new representation of resources. All communication must be stateless and cacheable.

There are four qualities of a RESTful interface:

- **Identify resources (URI in HTTP)** - use the same URI regardless of any operation.
- **Change with representations (Verbs in HTTP)** - use verbs, headers, and body.
- **Self-descriptive error message (status response in HTTP)** - Use status codes, don't reinvent the wheel.
- **[[]] (HTML interface for HTTP)** - your web service should be fully accessible in a browser.

Sample REST calls:

```
GET /someresources/anId

PUT /someresources/anId
{"anotherdata": "another value"}
```

REST is focused on exposing data. It minimizes the coupling between client/server and is often used for public HTTP APIs. REST uses a more generic and uniform method of exposing resources through URIs, [[headers]], and actions through verbs such as GET, POST, PUT, DELETE, and PATCH. Being stateless, REST is great for horizontal scaling and partitioning.

#### Disadvantage(s): REST
- With REST being focused on exposing data, it might not be a good fit if resources are not naturally organized or accessed in a simple hierarchy. For example, returning all updated records from the past hour matching a particular set of events is not easily expressed as a path. With REST, it is likely to be implemented with a combination of URI path, query parameters, and possibly the request body.
- REST typically relies on a few verbs (GET, POST, PUT, DELETE, and PATCH) which sometimes doesn't fit your use case. For example, moving expired documents to the archive folder might not cleanly fit within these verbs.
- Fetching complicated resources with nested hierarchies requires multiple round trips between the client and server to render single views, e.g. fetching content of a blog entry and the comments on that entry. For mobile applications operating in variable network conditions, these multiple roundtrips are highly undesirable.
- Over time, more fields might be added to an API response and older clients will receive all new data fields, even those that they do not need, as a result, it bloats the payload size and leads to larger latencies.

### RPC and REST calls comparison

|Operation|RPC|REST|
|---|---|---|
|Signup|**POST** /signup|**POST** /persons|
|Resign|**POST** /resign  <br>{  <br>"personid": "1234"  <br>}|**DELETE** /persons/1234|
|Read a person|**GET** /readPerson?personid=1234|**GET** /persons/1234|
|Read a person’s items list|**GET** /readUsersItemsList?personid=1234|**GET** /persons/1234/items|
|Add an item to a person’s items|**POST** /addItemToUsersItemsList  <br>{  <br>"personid": "1234";  <br>"itemid": "456"  <br>}|**POST** /persons/1234/items  <br>{  <br>"itemid": "456"  <br>}|
|Update an item|**POST** /modifyItem  <br>{  <br>"itemid": "456";  <br>"key": "value"  <br>}|**PUT** /items/456  <br>{  <br>"key": "value"  <br>}|
|Delete an item|**POST** /removeItem  <br>{  <br>"itemid": "456"  <br>}|**DELETE** /items/456|

_[[]]_

#### Source(s) and further reading: REST and RPC
- [[]]
- [[181186]]
- [[rest vs json rpc]]
- [[]]
- [[What are the drawbacks of using RESTful APIs]]
- [[2016 02 13 crack the system design interview]]
- [[]]
- [[viewtopic]]
# Gainz Open AI Backend

The test application is implemented in such a way that it can be run with no external dependencies. 
This is INTENTIONAL, as the aim is to showcase an OpenAI & Websockets integration, built as a FastAPI application.

### Setup & Installation
clone the project and run:
```sh
pip install -r requirements.txt
```

Once the project is installed, create a `.env` file at the root of the project, with the following variables:

| Key                      | Description                    |          |
|--------------------------|--------------------------------|----------|
| OPENAI_API_KEY           | Your Open AI API key           | Required |
| DATABASE_URI             | MongoDB Connection URI         | Optional |
| DATABASE_NAME            | MongoDB Database Name          | Optional |
| JWT_SECRET_KEY           | JWT secret key                 | Required |
| JWT_ALGORITHM            | JWT algorithm                  | Required |
| JWT_EXPIRES_IN_HOURS     | JWT expiry date in hours       | Required |

To run the application, execute the following command from the root directory of the application:
```sh
    uvicorn app.main:app --reload
```

### Completed Tasks
The rest and websocket endpoints of the app can be tested as a standalone using `postman`. 
This backend application implements the following tasks, per the test requirements:

- [x] **FastAPI Setup
  - [x] Initialize a new FastAPI project.
  - [x] Install required dependencies (fastapi, uvicorn, openai, websockets, etc.).
  - [x] Set up a basic project structure.
  
- [x] **Authentication**
  - [x] Implement JWT authentication/authorization middleware.
  - [x] Secure all endpoints with this authentication.
  
- [x] **OpenAI Integration**
  - [x] Set up OpenAI API credentials (use environment variables).
  - [x] Implement functions to interact with the Assistants API:
    - [x] Create or load an existing Assistant.
    - [x] Create a new thread.
    - [x] Add a Message to a Thread.
    - [x] Run the Assistant on a Thread.
    - [x] Retrieve the Assistant's response or stream it directly.
  - [x] Try to create more assistants and try to simulate them on a single thread (This is optional but appreciated if implemented).

- [x] **WebSocket Implementation**
  - [x] Create a WebSocket endpoint for client connections.
  - [x] Implement authentication/authorization for secure WebSocket connection.
  - [x] Implement logic to associate WebSocket connections with specific conversation threads.
  - [x] Handle multiple clients connected to the same thread.

- [x] **Streaming Implementation**
  - [x] Implement a mechanism to stream the Assistant's responses as they are generated.
  - [x] Ensure that streamed responses are sent to all clients connected to the relevant thread.

- [x] **API Endpoints**
  - [x] Create an endpoint to initialize a new conversation (creates a new Thread).
  - [x] Implement an endpoint to send a message to an existing Thread.
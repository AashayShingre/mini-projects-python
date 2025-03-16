from fastapi import FastAPI, Request
import uvicorn  # since it doesn't have app.run like flask. Rather run it with uvicorn
import argparse


app = FastAPI()


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"],
)
async def echoMessage(request: Request):
    body = await request.body()
    print(body)
    return {f"recieved {body.decode()} on {request.base_url}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy fast api application")
    parser.add_argument(
        "--port", type=int, default=8000, help="port for the server to listen to"
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to server for the server"
    )

    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)

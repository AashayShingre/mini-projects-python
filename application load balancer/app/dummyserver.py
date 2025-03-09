from fastapi import FastAPI
import uvicorn  # since it doesn't have app.run like flask. Rather run it with uvicorn
import argparse


app = FastAPI()


@app.get("/")
def getHome():
    return {"message": "Welcome"}


@app.post("/echo")
def echoMessage(data):
    return {f"recieved {data}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy fast api application")
    parser.add_argument(
        "-p", "--port", type=int, default=8000, help="port for the server to listen to"
    )
    parser.add_argument(
        "-h", "--host", default="0.0.0.0", help="Host to server for the server"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode (reload=True)"
    )

    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, reload=args.debug)

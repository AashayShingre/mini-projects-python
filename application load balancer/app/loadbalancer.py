from fastapi import FastAPI, Request, Response
import uvicorn
import argparse
from enum import Enum
import itertools
import httpx
from starlette.responses import StreamingResponse


def fetchArguments():
    parser = argparse.ArgumentParser(description="LoadBalancer with fast api")
    parser.add_argument("--port", type=int, default=7000, help="Port")
    parser.add_argument("--host", default="0.0.0.0", help="Host")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug tracing in fast api and also sets reload = True for uvicorn server",
    )

    return parser.parse_args()


UPSTREAM_SERVER = [("localhost", 8000), ("localhost", 8001), ("localhost", 8002)]

LOADBALANCING_ALGO = Enum(
    "LOADBALANCING_ALGO", ["ROUND_ROBIN", "LEAST_CONNECTIONS", "WEIGHTED_ROUND_ROBIN"]
)


def iteratorGenerator(method):
    if method == LOADBALANCING_ALGO.ROUND_ROBIN:
        return itertools.cycle(UPSTREAM_SERVER)

    raise Exception("Not yet implemented")


server_cycle = iteratorGenerator(LOADBALANCING_ALGO.ROUND_ROBIN)


args = fetchArguments()


app = FastAPI(debug=args.debug)


### STREAMS REQUEST/RESPONSE - doesn't buffer the request body (efficient for large requests/response)
### TODO : drops 10% of the time with httpx.ReadError
# @app.api_route(
#     "/{path:path}",
#     methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"],
# )
# async def forward_http(request: Request, path: str):
#     domain, port = next(server_cycle)
#     url = f"http://{domain}:{port}/{path}"
#     async with httpx.AsyncClient() as client:
#         req = client.build_request(
#             method=request.method,
#             url=url,
#             content=request.stream(),
#             headers=filter(lambda x: x[0] != b"host", request.headers.raw),
#         )
#         response = await client.send(req, stream=True)

#         return StreamingResponse(
#             content=response.aiter_bytes(),
#             status_code=response.status_code,
#             headers={
#                 x: y
#                 for x, y in dict(response.headers).items()
#                 if x not in ["date", "server", "content-length"]
#             },
#         )


### NON-STREAMING - Loads the full request body and then sends it
@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"],
)
async def forward_http(request: Request, path: str):
    domain, port = next(server_cycle)
    req_body = await request.body()
    url = f"http://{domain}:{port}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            content=req_body,
            headers=filter(lambda x: x[0] != b"host", request.headers.raw),
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={
                x: y
                for x, y in dict(response.headers).items()
                if x not in ["date", "server", "content-length"]
            },
        )


uvicorn.run(app, host=args.host, port=args.port, reload=args.debug)

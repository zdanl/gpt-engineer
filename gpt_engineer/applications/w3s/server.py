# Changelog
# * @ATheorell created this file
# * @zdanl here modiyfing @atheorell work from websockets to socket.io

from aiohttp import web
import socketio
import tempfile
import json
import os

from gpt_engineer.core.default.lean_agent import LeanAgent

# from gpt_engineer.core.preprompt_holder import PrepromptHolder

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*")
# sio.set('transports', ['websocket']);

app = web.Application()
sio.attach(app)

tempdir = tempfile.gettempdir()
agent = LeanAgent.with_default_config(tempdir)


class GPTEngineerNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print("Real-time socket to browser established.")
        await self.emit("openai_api_key", os.environ["OPENAI_API_KEY"])

    def on_disconnect(self, sid):
        print("Browser disconnected.")

    async def on_openai_api_key(self, sid, data):
        print(f"Received new OpenAI API Key: {data}")
        code = agent.seed(data)

    async def on_init(self, sid, prompt):
        print(f"Initializing: {prompt}")
        code = agent.init(prompt)
        await self.emit("init", json.dumps(code))

    async def on_improve(event, sid, data):
        print(f"{event}: {data}")
        code = agent.improve(json.loads(event["code"]), event["prompt"])
        await socketio.emit("improve", {"payload": json.dumps(code)})

    async def on_execute(event, sid, data):
        print(f"{event}: {data}")
        process = agent.execution_env.execute_program(event["code"])
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        error = stderr.decode("utf-8")
        payload = json.dumps({"output": output, "error": error})
        await socketio.emit("execute", {"payload": payload})


sio.register_namespace(GPTEngineerNamespace("/gpt-engineer"))


async def main():
    pass


if __name__ == "__main__":
    web.run_app(app, port=4444)

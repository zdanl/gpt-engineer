import { io } from 'socket.io-client';

declare var process : {
  env: {
    GPTENGINEER_SOCKETIO_HOST: string,
    GPTENGINEER_SOCKETIO_PORT: string
  }
}

const URL = `ws://${process.env.GPTENGINEER_SOCKETIO_HOST || "localhost"}:${process.env.GPTENGINEER_SOCKETIO_PORT || "4444"}/gpt-engineer`;

console.log(`Listenting at ${URL}`);

// autoConnect intentionally left at default: on
export const socket = io(URL, {transports: ['websocket'], upgrade: false});

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      GPTENGINEER_SOCKETIO_HOST: string;
      GPTENGINEER_SOCKETIO__PORT: string;
    }
  }
}

// If this file has no import/export statements (i.e. is a script)
// convert it into a module by adding an empty export statement.
export {}

/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_MODEL_API_HOST: string;
    readonly VITE_MODEL_API_PORT: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  
export class RestClientConfig {
    private targetHostname: string;
    private targetPort: string;

    private DEFAULT_TARGET_HOSTNAME = window.ENV.VITE_MODEL_API_HOST ?? 'localhost';
    private DEFAULT_TARGET_PORT = window.ENV.VITE_MODEL_API_PORT ?? '5000';

    constructor(targetHostname?: string, targetPort?: string) {
        this.targetHostname = targetHostname !== undefined ? targetHostname : this.DEFAULT_TARGET_HOSTNAME;
        this.targetPort = targetPort !== undefined ? targetPort : this.DEFAULT_TARGET_PORT;
    }

    public getTargetHostname(){
        return this.targetHostname
    }

    public getTargetPort() {
        return this.targetPort;
    }
}

export const useRestClientConfig = (targetHostname?: string, targetPort?: string) => new RestClientConfig(targetHostname, targetPort);
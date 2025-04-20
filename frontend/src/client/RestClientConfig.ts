class RestClientConfig {
    private targetHostname: string;
    private targetPort: string | undefined;

    private DEFAULT_TARGET_HOSTNAME = 'localhost';
    private DEFAULT_TARGET_PORT = '5000';

    constructor(targetHostname?: string, targetPort?: string) {
        this.targetHostname = targetHostname !== undefined ? targetHostname : this.DEFAULT_TARGET_HOSTNAME;
        this.targetPort = targetPort !== undefined ? targetPort : this.DEFAULT_TARGET_PORT;
    }

    public getTargetHostname(){
        return this.targetHostname
    }
}
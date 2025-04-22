import { RestClientConfig } from "@frontend/client/RestClientConfig";
import axios from 'axios';

export class RestClient {
    
    private clientConfig: RestClientConfig;

    constructor(clientConfig: RestClientConfig) {
        this.clientConfig = clientConfig;
    }

    public async doPost<T, B>(service:string, body: B): Promise<T> {
        const url = this.buildUrl(service)
        return await axios.post(url, body) 
    }

    private buildUrl(service: string) {
        const hostname = this.clientConfig.getTargetHostname()
        const port = this.clientConfig.getTargetPort()
        return `http://${hostname}:${port}/${service}`
    }

}

export const useRestClient = (clientConfig: RestClientConfig) => new RestClient(clientConfig);
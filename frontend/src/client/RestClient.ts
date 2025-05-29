import { RestClientConfig } from "@frontend/client/RestClientConfig";
import axios, { AxiosResponse } from 'axios';

export class RestClient {
    
    private clientConfig: RestClientConfig;

    constructor(clientConfig: RestClientConfig) {
        this.clientConfig = clientConfig;
    }

    public async doPost<T, B>(service:string, body: B): Promise<AxiosResponse<T>> {
        const url = this.buildUrl(service)
        return await axios.post(url, body) 
    }
    private buildUrl(service: string) {
        const url = this.clientConfig.getTargetUrl()
        return `${url}/${service}`
    }
}

export const useRestClient = (clientConfig: RestClientConfig) => new RestClient(clientConfig);
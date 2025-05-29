import { RestClientConfig } from "@frontend/client/RestClientConfig";
import axios, { AxiosResponse } from 'axios';

export class RestClient {
    
    constructor() {
    }

    public async doPost<T, B>(service:string, body: B): Promise<AxiosResponse<T>> {
        const url = this.buildUrl(service)
        return await axios.post(url, body) 
    }
    private buildUrl(service: string) {
        return `/api/${service}`
    }
}

export const useRestClient = () => new RestClient();
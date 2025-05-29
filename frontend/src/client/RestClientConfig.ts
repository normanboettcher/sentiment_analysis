export class RestClientConfig {
    private targetUrl: string;

    private DEFAULT_TARGET_URL =
    (window.ENV && window.ENV.VITE_MODEL_API_URL !== undefined
        && window.ENV.VITE_MODEL_API_URL !== "") ? window.ENV.VITE_MODEL_API_URL : 'http://localhost:5000';

    constructor(targetUrl?: string) {
        this.targetUrl = targetUrl !== undefined ? targetUrl : this.DEFAULT_TARGET_URL;
    }

    public getTargetUrl(){
        return this.targetUrl
    }
}

export const useRestClientConfig = (targetUrl?: string) => new RestClientConfig(targetUrl);
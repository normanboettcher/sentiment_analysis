import { SentimentResponse } from "./Response";

export class ResponseValidator {
    constructor(){}

    public isErrorResponse(res: SentimentResponse) {
        return 'error' in res;
    }

}

export const useResponseValidator = () => new ResponseValidator();
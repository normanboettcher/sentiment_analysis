import { SentimentResponse } from "./Response";

export class ResponseValidator {

    public isErrorResponse(res: SentimentResponse): boolean{
        return res.error !== undefined;
    }

}

export const useResponseValidator = () => new ResponseValidator();
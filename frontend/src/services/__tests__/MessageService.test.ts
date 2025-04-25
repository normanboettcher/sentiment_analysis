import {it, describe, expect} from 'vitest'
import { IMessageService } from '../IMessageService'
import { useSentimentMessageService } from '../MessageService'
import MessageFactory from '../MessageFactory'

describe('Testcases for getMessageFromSentiment', () => {
    it.each(['positive', 'negative'])(`should return a valid message for given sentiment is %s`, (sentiment) => {
        const messageService: IMessageService = useSentimentMessageService()
        //@ts-ignore
        const result = messageService.getMessageFromSentiment(sentiment);
        //@ts-ignore
        expect(result).toBe(MessageFactory.getMessage(sentiment));
    })
})
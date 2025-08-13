/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExtraResponse } from '../models/ExtraResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ExtrasService {
    /**
     * Get Extras
     * Get all available extras.
     * @returns ExtraResponse Successful Response
     * @throws ApiError
     */
    public static getExtras(): CancelablePromise<Array<ExtraResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/extras/',
        });
    }
}

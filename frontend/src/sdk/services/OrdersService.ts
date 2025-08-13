/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderCreate } from '../models/OrderCreate';
import type { OrderResponse } from '../models/OrderResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class OrdersService {
    /**
     * Create Order
     * Create a new order.
     * @param requestBody
     * @returns OrderResponse Successful Response
     * @throws ApiError
     */
    public static createOrder(
        requestBody: OrderCreate,
    ): CancelablePromise<OrderResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/orders/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}

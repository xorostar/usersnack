/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FoodItemResponse } from '../models/FoodItemResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class FoodItemsService {
    /**
     * Get Food Items
     * Get all food items with their ingredients.
     * @returns FoodItemResponse Successful Response
     * @throws ApiError
     */
    public static getFoodItems(): CancelablePromise<Array<FoodItemResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/food-items/',
        });
    }
    /**
     * Get Food Item
     * Get a specific food item with its ingredients.
     * @param foodItemId
     * @returns FoodItemResponse Successful Response
     * @throws ApiError
     */
    public static getFoodItem(
        foodItemId: string,
    ): CancelablePromise<FoodItemResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/food-items/{food_item_id}',
            path: {
                'food_item_id': foodItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}

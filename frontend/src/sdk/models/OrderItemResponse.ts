/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExtraInResponse } from './ExtraInResponse';
/**
 * Response model for order item information.
 */
export type OrderItemResponse = {
    /**
     * Unique identifier of the food item
     */
    food_item_id: string;
    /**
     * Name of the food item
     */
    food_item_name: string;
    /**
     * Quantity ordered
     */
    quantity: number;
    /**
     * Unit price of the food item
     */
    unit_price: string;
    /**
     * List of extras added to this item
     */
    extras: Array<ExtraInResponse>;
    /**
     * Total price for this line item
     */
    line_total: string;
};


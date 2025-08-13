/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Request model for creating an order item.
 */
export type OrderItemCreate = {
    /**
     * Unique identifier of the food item
     */
    food_item_id: string;
    /**
     * Quantity of the food item
     */
    quantity: number;
    /**
     * List of extra IDs to add to this item
     */
    extra_ids?: Array<string>;
};


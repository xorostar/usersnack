/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { IngredientResponse } from './IngredientResponse';
/**
 * Response model for food item information.
 */
export type FoodItemResponse = {
    /**
     * Unique identifier for the food item
     */
    id: string;
    /**
     * Name of the food item
     */
    name: string;
    /**
     * Category of the food item
     */
    category: string;
    /**
     * Base price of the food item
     */
    base_price: string;
    /**
     * URL to the food item image
     */
    image?: (string | null);
    /**
     * Timestamp when the food item was created
     */
    created_at: string;
    /**
     * List of ingredients in the food item
     */
    ingredients: Array<IngredientResponse>;
};


/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderItemResponse } from './OrderItemResponse';
/**
 * Response model for order information.
 */
export type OrderResponse = {
    /**
     * Unique identifier for the order
     */
    id: string;
    /**
     * Current status of the order
     */
    status: string;
    /**
     * Currency used for the order
     */
    currency: string;
    /**
     * Customer's full name
     */
    customer_name: string;
    /**
     * Customer's delivery address
     */
    customer_address: string;
    /**
     * List of order items
     */
    items: Array<OrderItemResponse>;
    /**
     * Total amount for the entire order
     */
    total_amount: string;
    /**
     * ISO timestamp when the order was created
     */
    created_at: string;
};


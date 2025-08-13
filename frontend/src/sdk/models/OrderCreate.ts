/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Currency } from './Currency';
import type { OrderItemCreate } from './OrderItemCreate';
/**
 * Request model for creating a new order.
 */
export type OrderCreate = {
    /**
     * List of order items
     */
    items: Array<OrderItemCreate>;
    /**
     * Currency for the order
     */
    currency: Currency;
    /**
     * Customer's full name
     */
    customer_name: string;
    /**
     * Customer's delivery address
     */
    customer_address: string;
};


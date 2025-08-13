import {
  FoodItemsService,
  ExtrasService,
  OrdersService,
  OpenAPI,
  type FoodItemResponse,
  type ExtraResponse,
  type OrderCreate,
  type OrderResponse,
} from "../sdk";

OpenAPI.BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export class ApiService {
  static async getFoodItems(): Promise<FoodItemResponse[]> {
    try {
      return await FoodItemsService.getFoodItems();
    } catch (error) {
      console.error("Error fetching food items:", error);
      throw error;
    }
  }

  static async getFoodItem(id: string): Promise<FoodItemResponse> {
    try {
      return await FoodItemsService.getFoodItem(id);
    } catch (error) {
      console.error("Error fetching food item:", error);
      throw error;
    }
  }

  static async getExtras(): Promise<ExtraResponse[]> {
    try {
      return await ExtrasService.getExtras();
    } catch (error) {
      console.error("Error fetching extras:", error);
      throw error;
    }
  }

  static async createOrder(order: OrderCreate): Promise<OrderResponse> {
    try {
      return await OrdersService.createOrder(order);
    } catch (error) {
      console.error("Error creating order:", error);
      throw error;
    }
  }
}

export const apiService = ApiService;

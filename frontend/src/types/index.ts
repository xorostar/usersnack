export type {
  IngredientResponse as Ingredient,
  FoodItemResponse as FoodItem,
  ExtraResponse as Extra,
  OrderItemCreate,
  OrderCreate,
  ExtraInResponse,
  OrderItemResponse,
  OrderResponse,
  Currency,
} from "../sdk";

export interface CustomerInfo {
  name: string;
  address: string;
}

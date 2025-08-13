import { useParams, useNavigate } from "react-router-dom";
import LoadingSpinner from "../components/LoadingSpinner";
import ExtraSelector from "../components/ExtraSelector";
import QuantitySelector from "../components/QuantitySelector";
import CustomerInfoForm from "../components/CustomerInfoForm";
import ProductImage from "../components/ProductImage";
import { Badge } from "@/components/ui/badge";
import { useProductOrder } from "../hooks";

const ProductOrderPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const {
    foodItem,
    extras,
    selectedExtras,
    quantity,
    loading,
    orderLoading,
    error,
    setSelectedExtras,
    setQuantity,
    handlePlaceOrder,
    calculateUnitPrice,
    calculateTotalPrice,
  } = useProductOrder({ productId: id });

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <LoadingSpinner />
      </div>
    );
  }

  if (error || !foodItem) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg mb-4">
          {error || "Product not found"}
        </div>
        <button
          onClick={() => navigate("/")}
          className="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 transition-colors"
        >
          Back to Menu
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Product Details - Takes 2/3 of the space */}
          <div className="xl:col-span-2 space-y-6">
            {/* Product Image and Basic Info */}
            <div className="bg-card rounded-lg shadow-sm border p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <ProductImage foodItem={foodItem} />

                <div className="space-y-4">
                  <div>
                    <h1 className="text-3xl font-bold mb-2">{foodItem.name}</h1>
                    <p className="text-2xl font-bold text-primary mb-4">
                      €{foodItem.base_price}
                    </p>
                    <Badge variant="outline" className="capitalize">
                      {foodItem.category}
                    </Badge>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold mb-3">Ingredients:</h3>
                    <div className="relative">
                      <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-2">
                        {foodItem.ingredients.map((ingredient) => (
                          <Badge
                            key={ingredient.id}
                            variant="secondary"
                            className="text-sm whitespace-nowrap flex-shrink-0"
                          >
                            {ingredient.name}
                          </Badge>
                        ))}
                      </div>
                      {/* Fade-out effect on the right */}
                      <div className="absolute right-0 top-0 bottom-2 w-8 bg-gradient-to-l from-background to-transparent pointer-events-none"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Order Configuration */}
            <div className="bg-card rounded-lg shadow-sm border p-6">
              <h2 className="text-xl font-semibold mb-6">
                Customize Your Order
              </h2>

              <div className="space-y-8">
                <div>
                  <h3 className="text-lg font-medium mb-4">Quantity</h3>
                  <QuantitySelector
                    quantity={quantity}
                    onQuantityChange={setQuantity}
                  />
                </div>

                <div>
                  <h3 className="text-lg font-medium mb-4">Extras</h3>
                  <ExtraSelector
                    extras={extras}
                    selectedExtras={selectedExtras}
                    onExtrasChange={setSelectedExtras}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Sticky Order Summary - Takes 1/3 of the space */}
          <div className="xl:col-span-1">
            <div className="sticky top-6 space-y-6">
              <div className="bg-card rounded-lg shadow-sm border p-6">
                <h2 className="text-xl font-semibold mb-6">Order Summary</h2>

                <div className="space-y-4 mb-6">
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Base Price:</span>
                    <span className="font-medium">€{foodItem.base_price}</span>
                  </div>

                  {selectedExtras.length > 0 && (
                    <div className="flex justify-between items-center">
                      <span className="text-muted-foreground">Extras:</span>
                      <span className="font-medium">
                        €
                        {selectedExtras
                          .reduce(
                            (sum, extra) => sum + parseFloat(extra.price),
                            0
                          )
                          .toFixed(2)}
                      </span>
                    </div>
                  )}

                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Unit Price:</span>
                    <span className="font-semibold">
                      €{calculateUnitPrice().toFixed(2)}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Quantity:</span>
                    <span className="font-medium">{quantity}</span>
                  </div>

                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center">
                      <span className="text-lg font-semibold">Total:</span>
                      <span className="text-2xl font-bold text-primary">
                        €{calculateTotalPrice().toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Customer Information Form */}
              <div className="bg-card rounded-lg shadow-sm border p-6">
                <h2 className="text-xl font-semibold mb-6">
                  Delivery Information
                </h2>
                <CustomerInfoForm
                  onSubmit={handlePlaceOrder}
                  loading={orderLoading}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductOrderPage;

import { Button } from "@/components/ui/button";

interface QuantitySelectorProps {
  quantity: number;
  onQuantityChange: (quantity: number) => void;
  min?: number;
  max?: number;
}

const QuantitySelector = ({
  quantity,
  onQuantityChange,
  min = 1,
  max = 10,
}: QuantitySelectorProps) => {
  const handleIncrement = () => {
    if (quantity < max) {
      onQuantityChange(quantity + 1);
    }
  };

  const handleDecrement = () => {
    if (quantity > min) {
      onQuantityChange(quantity - 1);
    }
  };

  return (
    <div className="flex items-center space-x-3">
      <Button
        onClick={handleDecrement}
        disabled={quantity <= min}
        variant="outline"
        size="icon"
        className="w-10 h-10 rounded-full cursor-pointer"
      >
        -
      </Button>

      <span className="text-xl font-semibold min-w-[3rem] text-center">
        {quantity}
      </span>

      <Button
        onClick={handleIncrement}
        disabled={quantity >= max}
        size="icon"
        className="w-10 h-10 rounded-full cursor-pointer"
      >
        +
      </Button>
    </div>
  );
};

export default QuantitySelector;
